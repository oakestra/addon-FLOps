import api.request_management.custom_http as custom_http
import api.request_management.custom_requests as custom_requests
import utils.classes.exceptions as custom_exceptions
from api.utils.auxiliary import get_matching_type
from api.utils.consts import SYSTEM_MANAGER_URL
from flops.classes.abstract.base import FlOpsBaseClass
from utils.classes.exceptions import ProjectServiceAppend
from utils.types import SLA, ServiceId


def append_service_to_flops_project(
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
            exception=ProjectServiceAppend,
        ),
    ).execute()
    from icecream import ic

    ic("RRRRRRRRR", response)
    # return new_app


def deploy_service(service_id: ServiceId, matching_caller_object: FlOpsBaseClass = None) -> None:
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
