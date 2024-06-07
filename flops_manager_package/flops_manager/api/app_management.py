from flops_manager.api.request_management.custom_http import HttpMethods
from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.api.utils.auxiliary import get_matching_type
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_manager.utils.types import SLA, Application
from pydantic import BaseModel


def create_app(
    sla: SLA,
    flops_project_id: str = None,
    bearer_token: str = None,
    matching_caller_object: BaseModel = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    # NOTE: The called endpoint returns all apps of the user not just the newest inserted one.
    response = CustomRequest(
        core=RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=sla,
            custom_headers={"Authorization": bearer_token} if bearer_token else None,
        ),
        aux=RequestAuxiliaries(
            what_should_happen=f"Create new {app_type }application",
            show_msg_on_success=True,
            flops_exception_type=FlOpsExceptionTypes.APP_CREATE,
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
        raise FLOpsManagerException(
            flops_exception_type=FlOpsExceptionTypes.APP_CREATE,
            flops_project_id=flops_project_id,
            text=f"Could not find new {app_type } app after creating it",
        )

    return new_app


def fetch_app_from_orchestrator(
    app_id: str,
    matching_caller_object: BaseModel = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    response = CustomRequest(
        core=RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{app_id}",
        ),
        aux=RequestAuxiliaries(
            what_should_happen=f"Fetch {app_type} app '{app_id}'",
            flops_exception_type=FlOpsExceptionTypes.APP_FETCH,
            show_msg_on_success=True,
        ),
    ).execute()
    return response
