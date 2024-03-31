from http import HTTPStatus

import api.utils
from fl_ui_management.notification import notify_ui
from image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from image_builder_management.util import generate_builder_sla
from utils.exceptions import (
    BuilderAppCreationException,
    BuilderAppDeletionException,
    BuilderServiceDeploymentException,
)
from utils.identifier import FlOpsIdentifier
from utils.logging import logger


def delegate_image_build(
    flops_identifier: FlOpsIdentifier, ml_repo: MlRepo, verbose: bool = False
) -> None:

    if verbose:
        notify_ui(
            "New FL Client image needs to be build. Start build delegation processes.",
            flops_identifier,
        )

    builder_app_sla = generate_builder_sla(ml_repo, flops_identifier)
    builder_app_name = builder_app_sla["applications"][0]["application_name"]
    logger.debug(f"Created builder SLA based on '{ml_repo.url}': {builder_app_sla}")

    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint="/api/application",
        data=builder_app_sla,
        what_should_happen=f"Create new builder app '{flops_identifier.flops_id}'-'{ml_repo.url}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppCreationException()

    if verbose:
        notify_ui(
            "New Builder application created",
            flops_identifier,
        )

    new_builder_app = next(
        (app for app in json_data if app["application_name"] == builder_app_name), None
    )
    if new_builder_app is None:
        raise BuilderAppCreationException()
    builder_service_id = new_builder_app["microservices"][0]

    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint=f"/api/service/{builder_service_id}/instance",
        what_should_happen=f"Deploy builder service for '{ml_repo.url}', id '{builder_service_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderServiceDeploymentException()

    if verbose:
        notify_ui(
            "New Builder application deployed & started",
            flops_identifier,
        )


def fetch_builder_app(flops_id: str) -> dict:
    query_params = f"app_name=bu{flops_id}&app_namespace={BUILDER_APP_NAMESPACE}"

    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        api_endpoint=f"/api/applications?{query_params}",
        what_should_happen=f"Fetch builder app bu'{flops_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppDeletionException()
    return json_data


def undeploy_builder_app(flops_id: str) -> None:
    builder_app = fetch_builder_app(flops_id)[0]

    builder_app_id = builder_app["applicationID"]

    status, _ = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.DELETE,
        api_endpoint=f"/api/application/{builder_app_id}",
        what_should_happen=f"Delete builder app for FLOps'{flops_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppDeletionException()


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
