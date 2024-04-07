import api.custom_http as custom_http
import api.custom_requests as custom_requests
import utils.classes.exceptions as custom_exceptions
from api.consts import SYSTEM_MANAGER_URL
from flops.classes.abstract.base import FlOpsBaseClass
from flops.classes.process import FlOpsProcess
from utils.types import SLA, Application, ServiceId


def _get_matching_type(matching_caller_object: FlOpsBaseClass) -> str:
    return (type(matching_caller_object).__name__ if matching_caller_object else "") + " "


def create_app(
    sla: SLA,
    flops_process: FlOpsProcess,
    bearer_token: str = None,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = _get_matching_type(matching_caller_object)
    flops_id = flops_process.flops_process_id
    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    response = custom_requests.CustomRequest(
        custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=sla,
            custom_headers={"Authorization": bearer_token} if bearer_token else None,
        ),
        custom_requests.RequestAuxiliaries(
            what_should_happen=f"Create new {app_type }application '{flops_id}'",
            flops_process=flops_process,
            show_msg_on_success=True,
            exception=custom_exceptions.AppCreationException,
        ),
    ).execute()
    new_app = next(
        (
            response_app
            for response_app in response
            if response_app["application_name"]
            in [sla_app["application_name"] for sla_app in sla["applications"]]
        ),
        None,
    )
    if new_app is None:
        raise custom_exceptions.AppCreationException(
            f"Could not find new {app_type } app after creating it", flops_process
        )
    return new_app


def deploy_service(service_id: ServiceId, matching_caller_object: FlOpsBaseClass = None) -> None:
    service_type = _get_matching_type(matching_caller_object)
    custom_requests.CustomRequest(
        custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{service_id}/instance",
        ),
        custom_requests.RequestAuxiliaries(
            what_should_happen=f"Deploy {service_type }service '{service_id}'",
            exception=custom_exceptions.ServiceDeploymentException,
            show_msg_on_success=True,
        ),
    ).execute()


def fetch_app(
    flops_process_id: str,
    app_namespace: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = _get_matching_type(matching_caller_object)
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{app_namespace}/bu{flops_process_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Fetch {app_type} app bu'{flops_process_id}'",
            exception=custom_exceptions.AppFetchException,
            show_msg_on_success=True,
        ),
    ).execute()
    return response


def undeploy(
    application_id: str,
    flops_process_id: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> None:
    app_type = _get_matching_type(matching_caller_object)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.DELETE,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{application_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Delete {app_type} app for FLOps'{flops_process_id}'",
            exception=custom_exceptions.AppDeletionException,
            show_msg_on_success=True,
        ),
    ).execute()
