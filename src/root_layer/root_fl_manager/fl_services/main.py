import secrets
from http import HTTPStatus
from typing import Dict, Tuple

import api.utils
from image_builder_management.common import MlRepo
from image_builder_management.main import delegate_image_build, undeploy_builder_app
from image_registry.main import fetch_latest_matching_image
from utils.exceptions import (
    FLUIServiceCreationException,
    FLUIServiceDeploymentException,
    GetMLServiceException,
)
from utils.logging import logger
from utils.sla_generator import generate_sla
from utils.types import DB_SERVICE_OBJECT, FL_SLA, SERVICE_ID


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


def create_fl_ui_service(new_fl_service_sla: FL_SLA, bearer_token: str) -> Tuple[SERVICE_ID, str]:
    unique_identifier = secrets.token_urlsafe(4)

    fl_ui_service_SLA = generate_sla(
        customerID=new_fl_service_sla["customerID"],
        app_name=unique_identifier,
        app_namespace="fl_app",
        service_name=unique_identifier,
        service_namespace="fl_ui",
        code="docker.io/efrecon/mqtt-client:latest",  # TODO
        # cmd=f"mosquitto_sub -h 192.168.178.44 -p 9027 -t {original_ml_service_id}/ui",
        memory=500,
        storage=0,
        vcpus=1,
    )

    logger.debug("AAAAAAAAAAAAAA")
    logger.debug(fl_ui_service_SLA)

    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        headers={"Authorization": bearer_token},
        data=fl_ui_service_SLA,
        api_endpoint="/api/application/",
        what_should_happen=f"Create new FL service '{unique_identifier}' with FL UI service",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceCreationException()

    return json_data["microserviceID"], unique_identifier


def handle_new_fl_service(new_fl_service_sla: FL_SLA, auth_header: str) -> None:
    fl_ui_service_id, unique_identifier = create_fl_ui_service(new_fl_service_sla, auth_header)
    return

    status, _ = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint=f"/api/service/{fl_ui_service_id}/instance",
        what_should_happen=f"Deploy FL UI service '{fl_ui_service_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceDeploymentException()

    ml_repo = MlRepo(new_fl_service_sla["code"])
    status, latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if status != HTTPStatus.OK:
        logger.critical(f"Failed to check latest image based on this repo name: '{ml_repo.name}'")
        return

    if latest_matching_image_name is not None:
        # TODO update_service_image(new_fl_service, existing_image_name)
        # TODO logger.info(f"FL service '{service_id}' has been properly prepared")
        return

    return
    delegate_image_build(unique_identifier, ml_repo)


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
