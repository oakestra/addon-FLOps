import flops.fl_ui_management.notification as ui_notifier
import flops.main
from flops.image_builder_management.app import (
    create_image_builder,
    deploy_builder_service,
    undeploy_builder_app,
)
from flops.image_builder_management.common import MlRepo
from flops.process import FlOpsProcess
from utils.logging import logger


def delegate_image_build(
    flops_process: FlOpsProcess,
    ml_repo: MlRepo,
    verbose: bool = False,
) -> None:
    if verbose:
        ui_notifier.notify_ui(
            "New FL Client image needs to be build. Start build delegation processes.",
            flops_process,
        )
    builder_service_id = create_image_builder(flops_process, ml_repo, verbose)
    deploy_builder_service(builder_service_id, ml_repo, flops_process, verbose)


def handle_builder_success(builder_success_msg: dict) -> None:
    logger.debug(builder_success_msg)
    image_name_with_tag = builder_success_msg["image_name_with_tag"]
    flops_process_id = builder_success_msg["flops_process_id"]
    undeploy_builder_app(flops_process_id)
    flops.main.handle_fl_operations(FlOpsProcess(flops_process_id), image_name_with_tag)


def handle_builder_failed(builder_failed_msg: dict) -> None:
    logger.debug(builder_failed_msg)
    flops_process_id = builder_failed_msg["flops_process_id"]
    undeploy_builder_app(flops_process_id)
    msg = "Builder failed. Terminating this FLOps."
    logger.critical(msg)
    ui_notifier.notify_ui(msg, FlOpsProcess(flops_process_id))
