import mqtt.main
from flops.classes.abstract.deyployable import FlOpsDeployableClass
from flops.classes.ml_repo import MlRepo
from flops.classes.process import FlOpsProcess
from flops.classes.ui import FLUserInterface
from flops.image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from pydantic import Field
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)


class FLClientEnvImageBuilder(FlOpsDeployableClass):
    flops_process: FlOpsProcess = Field(None, exclude=True, repr=False)
    ui: FLUserInterface = Field(None, exclude=True, repr=False)
    ml_repo: MlRepo = Field(None, exclude=True, repr=False)

    ip: str = Field("", init=False)

    flops_process_id: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_process_id = self.flops_process.flops_process_id
        self._configure_sla_components()

    def _configure_sla_components(self) -> None:
        BUILDER_APP_NAMESPACE = "flbuild"
        builder_name = f"bu{self.flops_process.get_shortened_id()}"
        cmd = " ".join(
            (
                "python3",
                "main.py",
                self.ml_repo.url,
                ROOT_FL_IMAGE_REGISTRY_URL,
                self.flops_process_id,
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


# def handle_builder_success(builder_success_msg: dict) -> None:
#     logger.debug(builder_success_msg)
#     image_name_with_tag = builder_success_msg["image_name_with_tag"]
#     flops_process_id = builder_success_msg["flops_process_id"]

#     undeploy_builder_app(flops_process_id)
#     flops.main.handle_fl_operations(FlOpsProcess(flops_process_id), image_name_with_tag)


# def handle_builder_failed(builder_failed_msg: dict) -> None:
#     logger.debug(builder_failed_msg)
#     flops_process_id = builder_failed_msg["flops_process_id"]
#     undeploy_builder_app(flops_process_id)
#     msg = "Builder failed. Terminating this FLOps."
#     logger.critical(msg)
#     ui_notifier.notify_ui(msg, FlOpsProcess(flops_process_id))
