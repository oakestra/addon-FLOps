import fl_ui_management.notification as ui_notifier
from flops.identifier import FlOpsIdentifier
from image_builder_management.app import (
    create_new_image_builder_app,
    deploy_builder_service,
    undeploy_builder_app,
)
from image_builder_management.common import MlRepo
from utils.logging import logger


def delegate_image_build(
    flops_identifier: FlOpsIdentifier,
    ml_repo: MlRepo,
    verbose: bool = False,
) -> None:
    if verbose:
        ui_notifier.notify_ui(
            "New FL Client image needs to be build. Start build delegation processes.",
            flops_identifier,
        )
    builder_service_id = create_new_image_builder_app(flops_identifier, ml_repo, verbose)
    deploy_builder_service(builder_service_id, ml_repo, flops_identifier, verbose)


def handle_builder_success(builder_success_msg: dict) -> None:
    # origin_fl_service_id = builder_success_msg["service_id"]
    # image_name_with_tag = builder_success_msg["image_name_with_tag"]
    logger.debug("000000")
    logger.debug(builder_success_msg)
    logger.debug("111111")
    flops_id = builder_success_msg["flops_id"]
    undeploy_builder_app(flops_id)
    # TODO continue with further FL steps


def handle_builder_failed(builder_failed_msg: dict) -> None:
    logger.debug("AA")
    logger.debug(builder_failed_msg)

    flops_id = builder_failed_msg["flops_id"]
    undeploy_builder_app(flops_id)

    logger.debug("ZZ")
