from typing import Optional

from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX
from flops_manager.utils.env_vars import ML_DATA_SERVER_PORT
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import BaseModel, Field


class _MockDataConfiguration(BaseModel):
    dataset_name: str = Field(
        default="mnist",
        description="The name of the dataset to be loaded from the underlying dataset provider.",
    )
    number_of_partitions: int = Field(
        default=1,
        description=" ".join(
            (
                "The dataset is usually fetched as a whole and then split into partitions.",
                "If the number of partitions is 1 then the whole dataset will be used.",
            )
        ),
    )
    # NOTE: The idea is to allow two uses for the mock data provider.
    # 1) Where a single mock service will provide all the data partitions.
    # 2) One partition will be handled by one mock service (more "realistic").
    #    The multiple services will be spawned up by the FLOps Manager.
    partition_index: Optional[int] = Field(
        default=None,
        description=" ".join(
            (
                "If provided the mock will only use this one partition.",
                "E.g. If number_of_partitions=3 and partition_index=1",
                "the mock will split the dataset into 3 parts and only send the 2nd to the server."
                "Else the mock will send all partitions to the server, piece by piece.",
            )
        ),
    )
    # NOTE: Currently this tag is just a file-name-prefix. Future work might organize these files
    # in a different manner (be it DB, FS, etc.) where adding metadata is natively supported.
    data_tag: str = Field(
        default="",
        description=" ".join(
            (
                "The stored data will be marked with this tag to differentiate it easily.",
                "Learner services also use these data_tags to query all found data",
                "matching these tags from the ml-data-server.",
                "These tags enable us to differentiate between different use-cases,",
                "e.g. FLOps projects",
            )
        ),
    )


class MockDataProvider(FLOpsService):
    namespace = "mockdp"
    parent_app: FLOpsHelperApp = Field(None, exclude=True, repr=False)

    mock_data_configuration: _MockDataConfiguration = _MockDataConfiguration()

    def _configure_sla_components(self) -> None:
        service_name = f"mockdp{get_shortened_unique_id(self.parent_app.app_id)}"
        cmd = " ".join(
            (
                FLOPS_SERVICE_CMD_PREFIX,
                self.mock_data_configuration.dataset_name,
                str(self.mock_data_configuration.number_of_partitions),
                self.mock_data_configuration.data_tag,
                # TODO: add ip (instance IP) option to specify where exactly
                # to send mock data to
            )
        )
        if self.mock_data_configuration.partition_index:
            cmd += f" {self.mock_data_configuration.partition_index}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.parent_app.customer_id,
                app_id=self.parent_app.app_id,
                names=SlaNames(
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-mock-data-provider:latest",
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(memory=200, vcpus=1, storage=0),
                port=str(ML_DATA_SERVER_PORT),
            ),
        )
