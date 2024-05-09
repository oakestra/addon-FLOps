from flops_manager.classes.deployables.project_services.base import FLOpsProjectService
from flops_manager.classes.deployables.ui import FLOpsUserInterface
from flops_manager.mqtt.constants import FLOPS_MQTT_BROKER_IP
from flops_manager.mqtt.sender import notify_ui
from flops_manager.registry_management import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.utils.common import get_shortened_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
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
    ui: FLOpsUserInterface = Field(None, exclude=True, repr=False)

    namespace = "builder"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New FLOps images need to be build. Start build delegation processes.",
            )

        super().model_post_init(_)

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New Builder service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        cmd = " ".join(
            (
                "python3",
                "main.py",
                self.flops_project.ml_model_flavor,
                self.flops_project.ml_repo_info.url,
                FLOPS_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.ui.ip,
            )
        )
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.flops_project.app_name,
                    app_namespace=self.flops_project.namespace,
                    service_name=f"builder{get_shortened_id(self.flops_project)}",
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
