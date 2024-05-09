from typing import List

from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.classes.project import FLOpsProject
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes

FLOPS_IMAGE_REGISTRY_PORT = "5073"
# TODO find a way to make this dynamic and practical instead of a hardcode !
FLOPS_IMAGE_REGISTRY_IP = "192.168.178.44"
FLOPS_IMAGE_REGISTRY_URL = f"http://{FLOPS_IMAGE_REGISTRY_IP}:{FLOPS_IMAGE_REGISTRY_PORT}"


def check_registry_reachable(flops_project: FLOpsProject) -> bool:
    CustomRequest(
        core=RequestCore(
            base_url=FLOPS_IMAGE_REGISTRY_URL,
            api_endpoint="/api/application/",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Registry is reachable",
            flops_project_id=flops_project,
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
            show_msg_on_success=True,
        ),
    ).execute()
    return True


# Note: (image) repos are the "grouping" of all tags of a single image.
# E.g. The (image) repo "alpine" can have multiple tags "latest", "1.0.0", etc.
# We usually first check the image repo and then its tags.
def get_current_registry_image_repo_names() -> List[str]:
    response = CustomRequest(
        core=RequestCore(
            base_url=FLOPS_IMAGE_REGISTRY_URL,
            api_endpoint="/v2/_catalog",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get current registry repositories",
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        ),
    ).execute()
    return response["repositories"]


def get_current_tags_for_image_in_registry(image_repo_name: str) -> List[str]:
    response = CustomRequest(
        core=RequestCore(
            base_url=FLOPS_IMAGE_REGISTRY_URL,
            api_endpoint=f"/v2/{image_repo_name}/tags/list",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get image tags",
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        ),
    ).execute()
    return response["tags"]
