from http import HTTPStatus

import api.utils
from image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from image_builder_management.util import generate_builder_sla
from utils.exceptions import (
    BuilderAppCreationException,
    BuilderAppDeletionException,
    BuilderServiceDeploymentException,
)
from utils.logging import logger
from utils.types import SERVICE_ID


def delegate_image_build(original_ml_service_id: SERVICE_ID, ml_repo: MlRepo) -> None:

    builder_app_sla = generate_builder_sla(ml_repo, original_ml_service_id)
    builder_app_name = builder_app_sla["applications"][0]["application_name"]
    logger.debug(f"Created builder SLA based on '{ml_repo.url}': {builder_app_sla}")

    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint="/api/application",
        data=builder_app_sla,
        what_should_happen=f"Create new builder app for '{original_ml_service_id}'-'{ml_repo.url}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppCreationException()

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


def fetch_builder_app(builder_app_name: str) -> dict:
    query_params = f"app_name={builder_app_name}&app_namespace={BUILDER_APP_NAMESPACE}"
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        api_endpoint=f"/api/applications?{query_params}",
        what_should_happen=f"Fetch builder app '{builder_app_name}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppDeletionException()
    return json_data


def undeploy_builder_app(builder_app_name: str) -> None:
    builder_app = fetch_builder_app(builder_app_name)[0]

    builder_app_id = builder_app["applicationID"]

    status, _ = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.DELETE,
        api_endpoint=f"/api/application/{builder_app_id}",
        what_should_happen=f"Delete builder app '{builder_app_name}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise BuilderAppDeletionException()
