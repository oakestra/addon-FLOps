import api.custom_requests as custom_requests
import flops.fl_ui_management.notification as ui_notifier
import utils.exceptions
from api.consts import SYSTEM_MANAGER_URL
from api.custom_http import HttpMethod
from flops.image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from flops.image_builder_management.util import generate_builder_sla
from flops.process import FlOpsProcess
from utils.logging import logger
from utils.types import ServiceId


def create_new_image_builder_app(
    flops_process: FlOpsProcess,
    ml_repo: MlRepo,
    verbose: bool = False,
) -> ServiceId:
    builder_app_sla = generate_builder_sla(ml_repo, flops_process)
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
            what_should_happen=f"Create new builder '{flops_process.id}'-'{ml_repo.url}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()

    if verbose:
        ui_notifier.notify_ui(
            "New Builder application created",
            flops_process,
        )

    new_builder_app = next(
        (app for app in response if app["application_name"] == builder_app_name), None
    )
    if new_builder_app is None:
        raise utils.exceptions.ImageBuilderException(
            "Could not find new builder app after creating it", flops_process
        )

    return new_builder_app["microservices"][0]


def deploy_builder_service(
    builder_service_id: ServiceId,
    ml_repo: MlRepo,
    flops_process: FlOpsProcess,
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
            flops_process,
        )


def fetch_builder_app(flops_process_id: str) -> dict:
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{BUILDER_APP_NAMESPACE}/bu{flops_process_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Fetch builder app bu'{flops_process_id}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()
    return response


def undeploy_builder_app(flops_process_id: str) -> None:
    builder_app = fetch_builder_app(flops_process_id)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethod.DELETE,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{builder_app['applicationID']}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Delete builder app for FLOps'{flops_process_id}'",
            exception=utils.exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()
