from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.registry_management import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import Field


class FLOpsImageBuilder(FLOpsProjectService):
    namespace = "builder"
    project_observer_ip: str = Field(None, exclude=True, repr=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="New FLOps images need to be build. Start build delegation processes.",
            )

        super().model_post_init(_)

        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="New Builder service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        cmd = " ".join(
            (
                "python3",
                "main.py",
                self.parent_app.ml_model_flavor,
                self.parent_app.ml_repo_url,
                FLOPS_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,
            )
        )
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=f"builder{get_shortened_unique_id(self.parent_app.app_id)}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-image-builder:latest",
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(
                    memory=2000,
                    vcpus=1,
                    storage=15000,
                ),
            ),
        )
