from typing import Optional

from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX
from flops_manager.utils.env_vars import ML_DATA_SERVER_PORT
from flops_manager.utils.sla.components import (
    FLOPS_LEARNER_ADDON_TYPE,
    AddonConstraint,
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
    parent_app: Optional[FLOpsHelperApp] = Field(default=None, exclude=True, repr=False)

    mock_data_configuration: _MockDataConfiguration = _MockDataConfiguration()

    def _configure_sla_components(self) -> None:
        service_name = f"mockdp{get_shortened_unique_id(self.parent_app.app_id)}"  # type: ignore
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
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.parent_app.customer_id,  # type: ignore
                app_id=self.parent_app.app_id,  # type: ignore
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/oakestra/addon-flops/mock-data-provider:thesis",
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(memory=200, vcpus=1, storage=0),
                port=str(ML_DATA_SERVER_PORT),
                constraints=[AddonConstraint(needs=[FLOPS_LEARNER_ADDON_TYPE])],
            ),
        )
