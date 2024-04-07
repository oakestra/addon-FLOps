import api.request_management.custom_http as custom_http
import api.request_management.custom_requests as custom_requests
from api.utils.auxiliary import get_matching_type
from api.utils.consts import SYSTEM_MANAGER_URL
from flops.classes.abstract.base import FlOpsBaseClass
from utils.classes.exceptions import AppCreationException, AppDeletionException, AppFetchException
from utils.types import SLA, Application


def create_app(
    sla: SLA,
    flops_process_id: str,
    bearer_token: str = None,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=sla,
            custom_headers={"Authorization": bearer_token} if bearer_token else None,
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Create new {app_type }application '{flops_process_id}'",
            flops_process_id=flops_process_id,
            show_msg_on_success=True,
            exception=AppCreationException,
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
        raise AppCreationException(
            f"Could not find new {app_type } app after creating it", flops_process_id
        )
    return new_app


def fetch_app(
    flops_process_id: str,
    app_namespace: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{app_namespace}/bu{flops_process_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Fetch {app_type} app bu'{flops_process_id}'",
            exception=AppFetchException,
            show_msg_on_success=True,
        ),
    ).execute()
    return response


def undeploy_app(
    application_id: str,
    flops_process_id: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> None:
    app_type = get_matching_type(matching_caller_object)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.DELETE,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{application_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Delete {app_type} app for FLOps'{flops_process_id}'",
            exception=AppDeletionException,
            show_msg_on_success=True,
        ),
    ).execute()
