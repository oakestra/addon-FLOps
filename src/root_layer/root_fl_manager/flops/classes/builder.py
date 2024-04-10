import flops.main as main_flops
import mqtt.main
from flops.classes.abstract.oakestratable import FlOpsOakestraClass
from flops.classes.ml_repo import MlRepo
from flops.classes.project import FlOpsProject
from flops.classes.ui import FLUserInterface
from flops.image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from flops.utils import notify_ui
from pydantic import Field
from utils.common import FLOPS_USER_ACCOUNT
from utils.logging import logger
from utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)


class FLClientEnvImageBuilder(FlOpsOakestraClass):
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    ui: FLUserInterface = Field(None, exclude=True, repr=False)
    ml_repo: MlRepo = Field(None, exclude=True, repr=False)

    ip: str = Field("", init=False)

    flops_project_id: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        BUILDER_APP_NAMESPACE = "flbuild"
        builder_name = f"bu{self.flops_project.get_shortened_id()}"
        cmd = " ".join(
            (
                "python3",
                "main.py",
                self.ml_repo.url,
                ROOT_FL_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                # TODO need to figure out a way to provide
                # non docker-compose member exclusive DNS name as IP.
                # mqtt.main.ROOT_MQTT_BROKER_URL,
                "192.168.178.44",
                mqtt.main.ROOT_FL_MQTT_BROKER_PORT,
                self.ui.ip,
            )
        )

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=builder_name,
                    app_namespace=BUILDER_APP_NAMESPACE,
                    service_name=builder_name,
                    service_namespace=BUILDER_APP_NAMESPACE,
                ),
                compute=SlaCompute(
                    code="ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                app_desc="fl_plugin application for building FL client env images",
                resources=SlaResources(
                    memory=2000,
                    vcpus=1,
                    storage=15000,
                ),
            ),
        )

    @classmethod
    def handle_success(cls, builder_success_msg: dict) -> None:
        logger.debug(builder_success_msg)
        flops_project_id = builder_success_msg["flops_project_id"]
        cls.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
        main_flops.handle_fl_operations(
            flops_project=FlOpsProject.retrieve_from_db(flops_project_id=flops_project_id),
            fl_client_image=builder_success_msg["image_name_with_tag"],
        )

    @classmethod
    def handle_failed(cls, builder_failed_msg: dict) -> None:
        logger.debug(builder_failed_msg)
        flops_project_id = builder_failed_msg["flops_project_id"]
        cls.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
        msg = "Builder failed. Terminating this FLOps."
        logger.critical(msg)
        notify_ui(flops_project_id=flops_project_id, msg=msg)
