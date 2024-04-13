from flops_manager.classes.oakestratables.deployables.project_services.base import ProjectService
from flops_manager.image_registry.common import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.mqtt.constants import FLOPS_MQTT_BROKER_PORT
from flops_manager.mqtt.sender import notify_ui
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

from package.flops_manager.classes.oakestratables.deployables.ui import UserInterface
from package.flops_manager.classes.project_based.ml_repo import MlRepo
from package.flops_manager.classes.project_based.oakestrables.project import FlOpsProject


class FLLearnerImageBuilder(ProjectService):
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    ui: UserInterface = Field(None, exclude=True, repr=False)
    ml_repo: MlRepo = Field(None, exclude=True, repr=False)

    flops_project_id: str = Field("", init=False)

    namespace = "flbuild"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New FL Learner image needs to be build. Start build delegation processes.",
            )

        self.flops_project_id = self.flops_project.flops_project_id
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
                self.ml_repo.url,
                FLOPS_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                # TODO need to figure out a way to provide
                # non docker-compose member exclusive DNS name as IP.
                # mqtt.main.ROOT_MQTT_BROKER_URL,
                "192.168.178.44",
                FLOPS_MQTT_BROKER_PORT,
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
                    service_name=f"bu{self.flops_project.get_shortened_id()}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    # TODO rename image to "fl-learner-image-builder"
                    code="ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
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
