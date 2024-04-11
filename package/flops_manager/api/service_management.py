import flops_manager.api.request_management.custom_http as custom_http
import flops_manager.api.request_management.custom_requests as custom_requests
import flops_manager.utils.classes.exceptions as custom_exceptions
from flops_manager.api.utils.auxiliary import get_matching_type
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.flops.classes.abstract.base import FlOpsBaseClass
from flops_manager.utils.classes.exceptions import (
    FLOpsProjectServiceAppend,
    ServiceUnDeploymentException,
)
from flops_manager.utils.types import SLA, ServiceId


def append_service_to_flops_project_app(
    sla: SLA,
    flops_project_id: str,
    bearer_token: str = None,
    matching_caller_object: FlOpsBaseClass = None,
) -> ServiceId:
    service_type = get_matching_type(matching_caller_object)
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/service/",
            data=sla,
            custom_headers={"Authorization": bearer_token} if bearer_token else None,
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Append new {service_type }service {flops_project_id}",
            flops_project_id=flops_project_id,
            show_msg_on_success=True,
            exception=FLOpsProjectServiceAppend,
        ),
    ).execute()
    return response["job_id"]


def deploy(service_id: ServiceId, matching_caller_object: FlOpsBaseClass = None) -> None:
    service_type = get_matching_type(matching_caller_object)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{service_id}/instance",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Deploy {service_type }service '{service_id}'",
            exception=custom_exceptions.ServiceDeploymentException,
            show_msg_on_success=True,
        ),
    ).execute()


def undeploy(
    service_id: str,
    flops_project_id: str,
    matching_caller_object: FlOpsBaseClass = None,
) -> None:
    service_type = get_matching_type(matching_caller_object)
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=custom_http.HttpMethods.DELETE,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{service_id}",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Undeploy {service_type} service for FLOps'{flops_project_id}'",
            exception=ServiceUnDeploymentException,
            show_msg_on_success=True,
        ),
    ).execute()
