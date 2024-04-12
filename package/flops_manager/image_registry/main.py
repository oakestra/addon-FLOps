from typing import List, Optional

from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.classes.ml_repo import MlRepo
from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.image_registry.common import (
    FLOPS_IMAGE_REGISTRY_IP_WITH_PORT,
    FLOPS_IMAGE_REGISTRY_URL,
)
from flops_manager.image_registry.utils import get_latest_commit_hash
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes


def check_registry_reachable(flops_project: FlOpsProject) -> bool:
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
def get_current_registry_image_repos() -> List[str]:
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


def get_current_registry_repo_image_tags(ml_repo: MlRepo) -> List[str]:
    response = CustomRequest(
        core=RequestCore(
            base_url=FLOPS_IMAGE_REGISTRY_URL,
            api_endpoint=f"/v2/{ml_repo.get_sanitized_name()}/tags/list",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get image tags",
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        ),
    ).execute()
    return response["tags"]


def fetch_latest_matching_image(ml_repo: MlRepo) -> Optional[str]:
    current_image_reqpositories = get_current_registry_image_repos()
    if ml_repo.get_sanitized_name() not in current_image_reqpositories:
        return None
    current_image_tags = get_current_registry_repo_image_tags(ml_repo)
    latest_commit_hash = get_latest_commit_hash(ml_repo)
    return (
        f"{FLOPS_IMAGE_REGISTRY_IP_WITH_PORT}/{ml_repo.name}:{latest_commit_hash}"
        if latest_commit_hash in current_image_tags
        else None
    )
