from dataclasses import dataclass, field

import flops.fl_ui_management.notification as ui_notifier
import flops.main
from database.main import DbCollections
from flops.image_builder_management.common import MlRepo
from flops.image_builder_management.utils import generate_builder_sla
from flops.process import FlOpsProcess
from utils.classes.complex import FlOpsDeployableClass
from utils.logging import logger


@dataclass
class FLClientEnvImageBuilder(FlOpsDeployableClass):
    builder_app_id: str = field(init=False, default="")
    builder_service_id: str = field(init=False, default="")

    def __init__(self, flops_process: FlOpsProcess, ml_repo: MlRepo):
        if flops_process.verbose:
            ui_notifier.notify_ui(
                "New FL Client image needs to be build. Start build delegation processes.",
                flops_process,
            )
        super().__init__(DbCollections.IMAGE_BUILDERS, flops_process.flops_process_id)
        builder_sla = generate_builder_sla(ml_repo, flops_process)
        self._create(flops_process, builder_sla)
        self.__post_init__()

    def __post_init__(self, flops_process):
        super().__post_init__()
        if flops_process.verbose:
            ui_notifier.notify_ui(
                "New Builder application created & deployed",
                flops_process,
            )


# TODO
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
