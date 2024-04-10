import mqtt.main as main_mqtt
from flops.classes.abstract.customer_component import CustomerFacingComponent
from flops.classes.project import FlOpsProject
from flops.utils import generate_ip
from pydantic import Field
from utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)


class FLUserInterface(CustomerFacingComponent):
    # Note: Use the entire Project object instead but only store & display its id.
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    ip: str = Field("", init=False)

    namespace = "flui"

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
                    code="ghcr.io/malyuk-a/fl-ui:latest",
                    cmd=" ".join(
                        (
                            "python",
                            "main.py",
                            self.flops_project_id,
                            main_mqtt.ROOT_FL_MQTT_BROKER_URL,
                            main_mqtt.ROOT_FL_MQTT_BROKER_PORT,
                        )
                    ),
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,
                resources=SlaResources(memory=200, vcpus=1, storage=0),
            ),
        )
