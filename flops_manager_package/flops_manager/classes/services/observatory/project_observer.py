from flops_manager.classes.apps.observatory import FLOpsObservatory
from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.mqtt.constants import FLOPS_MQTT_BROKER_IP, FLOPS_MQTT_BROKER_PORT
from flops_manager.utils.common import generate_ip, get_shortened_id
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


class FLOpsProjectObserver(FLOpsService):
    namespace = "observ"

    parent_app: FLOpsObservatory = Field(None, exclude=True, repr=False)

    flops_project: FLOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        self.ip = generate_ip(self.flops_project_id, self)

        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        service_name = f"observ{get_shortened_id(self.flops_project.flops_project_id)}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.flops_project.customer_id,
                app_id=self.parent_app.app_id,
                names=SlaNames(
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-project-observer:latest",
                    cmd=" ".join(
                        (
                            FLOPS_SERVICE_CMD_PREFIX,
                            self.flops_project_id,
                            FLOPS_MQTT_BROKER_IP,
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
