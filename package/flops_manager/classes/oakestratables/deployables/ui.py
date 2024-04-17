from flops_manager.classes.oakestratables.deployables.project_based import (
    DeployableProjectBasedClass,
)
from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.mqtt.constants import FLOPS_MQTT_BROKER_PORT, FLOPS_MQTT_BROKER_URL
from flops_manager.utils.common import generate_ip
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import Field


class UserInterface(DeployableProjectBasedClass):
    # Note: Use the entire Project object instead but only store & display its id.
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    ip: str = Field("", init=False)

    namespace = "flopsui"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        self.ip = generate_ip(self.flops_project_id, self)

        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        name = f"ui{self.flops_project.get_shortened_id()}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.flops_project.customer_id,
                names=SlaNames(
                    # TODO adjust to be able to add this service to an existing customer app
                    # not just as a standalone app
                    app_name=name,
                    app_namespace=self.namespace,
                    service_name=name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-ui:latest",
                    cmd=" ".join(
                        (
                            FLOPS_SERVICE_CMD_PREFIX,
                            self.flops_project_id,
                            FLOPS_MQTT_BROKER_URL,
                            FLOPS_MQTT_BROKER_PORT,
                        )
                    ),
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,
                resources=SlaResources(memory=200, vcpus=1, storage=0),
            ),
        )
