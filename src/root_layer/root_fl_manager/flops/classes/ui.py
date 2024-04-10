import mqtt.main as main_mqtt
from flops.classes.abstract.oakestratable import FlOpsOakestraClass
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


class FLUserInterface(FlOpsOakestraClass):
    # Note: Use the entire Project object instead but only store & display its id.
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    bearer_token: str = Field(exclude=True, repr=False)

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        self.ip = generate_ip(self.flops_project_id, self)
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.flops_project.customer_id,
                names=SlaNames(
                    app_name=f"fl{self.flops_project.get_shortened_id()}",
                    app_namespace="flui",
                    service_name=f"fl{self.flops_project.get_shortened_id()}",
                    service_namespace="flui",
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
