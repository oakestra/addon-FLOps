from http import HTTPStatus
from typing import Dict

import api.utils
from image_builder_management.common import MlRepo
from image_builder_management.main import delegate_image_build, undeploy_builder_app
from image_registry.main import fetch_latest_matching_image
from utils.exceptions import (
    FLUIServiceDeploymentException,
    GetMLServiceException,
    MLServiceReplacementException,
)
from utils.logging import logger
from utils.sla_generator import generate_sla
from utils.types import DB_SERVICE_OBJECT, SERVICE_ID


def fetch_ml_service(ml_service_id: SERVICE_ID) -> DB_SERVICE_OBJECT:
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.GET,
        api_endpoint=f"/api/service/{ml_service_id}",
        what_should_happen=f"Get ML service '{ml_service_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise GetMLServiceException()
    return json_data


def replace_original_ml_service_with_fl_ui(original_ml_service_id: SERVICE_ID) -> SERVICE_ID:
    ml_service = fetch_ml_service(original_ml_service_id)

    fl_service_SLA = generate_sla(
        app_name=ml_service["app_name"],
        app_namespace=ml_service["app_ns"],
        app_id=ml_service["applicationID"],
        service_name=f"flui{original_ml_service_id[-4:]}",
        service_namespace=ml_service["microservice_namespace"],
        code="docker.io/efrecon/mqtt-client:latest",
        cmd=f"mosquitto_sub -h 192.168.178.44 -p 9027 -t {original_ml_service_id}/ui",
        memory=500,
        storage=0,
        vcpus=1,
    )

    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.PUT,
        data=fl_service_SLA,
        api_endpoint=f"/api/service/{original_ml_service_id}",
        what_should_happen=f"Replace ML service '{original_ml_service_id}' with FL UI service",
        query_params="replace=true",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise MLServiceReplacementException()

    return json_data["microserviceID"]


def handle_new_fl_service(new_ml_service: Dict) -> None:
    original_ml_service_id = new_ml_service["microserviceID"]
    fl_ui_service_id = replace_original_ml_service_with_fl_ui(original_ml_service_id)

    status, _ = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint=f"/api/service/{fl_ui_service_id}/instance",
        what_should_happen=f"Deploy FL UI service instead of '{original_ml_service_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceDeploymentException()

    ml_repo = MlRepo(new_ml_service["code"])
    status, latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if status != HTTPStatus.OK:
        logger.critical(f"Failed to check latest image based on this repo name: '{ml_repo.name}'")
        return

    if latest_matching_image_name is not None:
        # TODO update_service_image(new_fl_service, existing_image_name)
        # TODO logger.info(f"FL service '{service_id}' has been properly prepared")
        return

    delegate_image_build(original_ml_service_id, ml_repo)


def handle_builder_success(builder_success_msg: Dict) -> None:
    # origin_fl_service_id = builder_success_msg["service_id"]
    # image_name_with_tag = builder_success_msg["image_name_with_tag"]
    logger.debug("000000")
    logger.debug(builder_success_msg)
    logger.debug("111111")
    builder_app_name = builder_success_msg["builder_app_name"]
    undeploy_builder_app(builder_app_name)
    # TODO continue with further FL steps


def handle_builder_failed(builder_failed_msg: Dict) -> None:
    logger.debug("AA")
    logger.debug(builder_failed_msg)

    builder_app_name = builder_failed_msg["builder_app_name"]
    undeploy_builder_app(builder_app_name)

    logger.debug("ZZ")
