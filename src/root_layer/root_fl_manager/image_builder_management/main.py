from image_builder_management.app import undeploy_builder_app
from utils.logging import logger


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
