from typing import Optional

from flops_manager.classes.apps.observatory import FLOpsObservatory
from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.utils.common import generate_ip, get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP, FLOPS_MQTT_BROKER_PORT
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

    parent_app: Optional[FLOpsObservatory] = Field(default=None, exclude=True, repr=False)

    flops_project: Optional[FLOpsProject] = Field(default=None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id  # type: ignore
        self.ip = generate_ip(self.flops_project_id, self)

        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        flops_project_id = self.flops_project.flops_project_id  # type: ignore
        service_name = f"observ{get_shortened_unique_id(flops_project_id)}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.flops_project.customer_id,  # type: ignore
                app_id=self.parent_app.app_id,  # type: ignore
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
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
                rr_ip=self.ip,  # type: ignore
                resources=SlaResources(memory=200, vcpus=1, storage=0),
            ),
        )
