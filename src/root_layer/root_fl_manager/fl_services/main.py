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
from utils.identifier import FlOpsIdentifier
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


def create_fl_ui_service(
    new_fl_service_sla: FL_SLA,
    bearer_token: str,
    flops_identifier: FlOpsIdentifier,
) -> SERVICE_ID:
    fl_ui_service_SLA = generate_sla(
        customerID=new_fl_service_sla["customerID"],
        app_name=f"fl{flops_identifier.flops_id}",
        app_namespace="flui",
        service_name=f"fl{flops_identifier.flops_id}",
        service_namespace="flui",
        code="ghcr.io/malyuk-a/fl-ui:latest",
        memory=200,
        storage=0,
        vcpus=1,
        rr_ip=flops_identifier.fl_ui_ip,
    )
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        headers={"Authorization": bearer_token},
        data=fl_ui_service_SLA,
        api_endpoint="/api/application/",
        what_should_happen=f"Create new FL UI service '{flops_identifier.flops_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceCreationException()

    return json_data[0]["microservices"][0]


def handle_new_fl_service(new_fl_service_sla: FL_SLA, auth_header: str) -> None:
    flops_identifier = FlOpsIdentifier()
    fl_ui_service_id = create_fl_ui_service(new_fl_service_sla, auth_header, flops_identifier)

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

    delegate_image_build(flops_identifier, ml_repo)


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
