from __future__ import annotations

from typing import TYPE_CHECKING

from flops_manager.api.request_management.custom_http import HttpMethods
from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.api.utils.auxiliary import get_matching_type
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.utils.exceptions import AppCreationException, AppFetchException
from flops_manager.utils.types import SLA, Application

if TYPE_CHECKING:
    from flops_manager.classes.base import FlOpsBaseClass


def create_app(
    sla: SLA,
    flops_project_id: str,
    bearer_token: str = None,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    response = CustomRequest(
        core=RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=sla,
            custom_headers={"Authorization": bearer_token} if bearer_token else None,
        ),
        aux=RequestAuxiliaries(
            what_should_happen=f"Create new {app_type }application {flops_project_id}",
            flops_project_id=flops_project_id,
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
            f"Could not find new {app_type } app after creating it", flops_project_id
        )
    return new_app


def fetch_app(
    flops_project_id: str,
    app_namespace: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> Application:
    app_type = get_matching_type(matching_caller_object)
    response = CustomRequest(
        core=RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/application/{app_namespace}/bu{flops_project_id}",
        ),
        aux=RequestAuxiliaries(
            what_should_happen=f"Fetch {app_type} app bu'{flops_project_id}'",
            exception=AppFetchException,
            show_msg_on_success=True,
        ),
    ).execute()
    return response
