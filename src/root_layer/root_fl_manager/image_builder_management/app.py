import api.custom_requests as custom_requests
import fl_ui_management.notification as ui_notifier
import utils.exceptions
from api.consts import SYSTEM_MANAGER_URL
from api.custom_http import HttpMethod
from flops.identifier import FlOpsIdentifier
from image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from image_builder_management.util import generate_builder_sla
from utils.logging import logger
from utils.types import ServiceId


def create_new_image_builder_app(
    flops_identifier: FlOpsIdentifier,
    ml_repo: MlRepo,
    verbose: bool = False,
) -> ServiceId:
    builder_app_sla = generate_builder_sla(ml_repo, flops_identifier)
    builder_app_name = builder_app_sla["applications"][0]["application_name"]
    logger.debug(f"Created builder SLA based on '{ml_repo.url}': {builder_app_sla}")

    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethod.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application",
            data=builder_app_sla,
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Create new builder '{flops_identifier.flops_id}'-'{ml_repo.url}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()

    if verbose:
        ui_notifier.notify_ui(
            "New Builder application created",
            flops_identifier,
        )

    new_builder_app = next(
        (app for app in response if app["application_name"] == builder_app_name), None
    )
    if new_builder_app is None:
        raise utils.exceptions.ImageBuilderException(
            "Could not find new builder app after creating it", flops_identifier
        )

    return new_builder_app["microservices"][0]


def deploy_builder_service(
    builder_service_id: ServiceId,
    ml_repo: MlRepo,
    flops_identifier: FlOpsIdentifier,
    verbose: bool = False,
) -> None:
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethod.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{builder_service_id}/instance",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Deploy builder for '{ml_repo.url}', id '{builder_service_id}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()
    if verbose:
        ui_notifier.notify_ui(
            "New Builder application deployed & started",
            flops_identifier,
        )


def fetch_builder_app(flops_id: str) -> dict:
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{BUILDER_APP_NAMESPACE}/bu{flops_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Fetch builder app bu'{flops_id}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()
    return response


def undeploy_builder_app(flops_id: str) -> None:
    builder_app = fetch_builder_app(flops_id)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethod.DELETE,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{builder_app['applicationID']}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Delete builder app for FLOps'{flops_id}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()
