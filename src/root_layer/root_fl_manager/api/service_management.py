import api.request_management.custom_http as custom_http
import api.request_management.custom_requests as custom_requests
import utils.classes.exceptions as custom_exceptions
from api.utils.auxiliary import get_matching_type
from api.utils.consts import SYSTEM_MANAGER_URL
from flops.classes.abstract.base import FlOpsBaseClass
from utils.types import ServiceId


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
