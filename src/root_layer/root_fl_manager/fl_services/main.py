from http import HTTPStatus
from typing import Dict

from image_builder_management.main import delegate_image_build, undeploy_builder_app
from image_builder_management.repo_management import MlRepo
from image_registry.main import fetch_latest_matching_image
from utils.logging import logger


def handle_new_fl_service(new_fl_service: Dict) -> None:
    service_id = new_fl_service["microserviceID"]
    ml_repo = MlRepo(new_fl_service["code"])

    status, latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if status != HTTPStatus.OK:
        logger.critical(f"Failed to check latest image based on this repo name: '{ml_repo.name}'")
        return

    if latest_matching_image_name is not None:
        # TODO update_service_image(new_fl_service, existing_image_name)
        # TODO logger.info(f"FL service '{service_id}' has been properly prepared")
        return

    delegate_image_build(service_id, ml_repo)


def handle_builder_success(builder_success_msg: Dict) -> None:
    origin_fl_service_id = builder_success_msg["service_id"]
    image_name_with_tag = builder_success_msg["image_name_with_tag"]
    builder_app_name = builder_success_msg["builder_app_name"]
    undeploy_builder_app(builder_app_name)
    # TODO continue with further FL steps


def handle_builder_failed(builder_failed_msg: Dict) -> None:
    logger.debug("AA")
    logger.debug(builder_failed_msg)

    builder_app_name = builder_failed_msg["builder_app_name"]
    undeploy_builder_app(builder_app_name)

    logger.debug("ZZ")
