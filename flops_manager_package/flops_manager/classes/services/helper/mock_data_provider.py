from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX
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
    one_mock_service_per_partition: bool = Field(
        default=False,
        description=" ".join(
            (
                "If disabled one single mock service will be created.",
                "It will split the dataset into the number of specified partitions"
                "and send each partition ot the ml-data-server.",
                "If enabled one mock server per requested partition will be created",
                "to simulate multiple devices.",
            )
        ),
    )
    data_tags: str = Field(
        default="*",
        description=" ".join(
            (
                "The data will be stored with these data_tags to differentiate it easily.",
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
                    cmd=" ".join(
                        (
                            FLOPS_SERVICE_CMD_PREFIX,
                            # TODO: add the mock config params here
                            # TODO: add ip (instance IP) option to specify where exactly
                            # to send mock data to
                        )
                    ),
                ),
            ),
            details=SlaDetails(resources=SlaResources(memory=200, vcpus=1, storage=0)),
        )
