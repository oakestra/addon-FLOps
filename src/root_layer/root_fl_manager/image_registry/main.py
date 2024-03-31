from typing import List, Optional

from api.custom_requests import CustomRequest, RequestAuxiliaries, RequestCore
from image_builder_management.common import MlRepo
from image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from image_registry.utils import get_latest_commit_hash
from utils.exceptions import ImageRegistryException
from utils.identifier import FlOpsIdentifier


def check_registry_reachable(flops_identifier: FlOpsIdentifier) -> bool:
    CustomRequest(
        RequestCore(
            base_url=ROOT_FL_IMAGE_REGISTRY_URL,
            api_endpoint="/api/application/",
        ),
        RequestAuxiliaries(
            what_should_happen="Registry is reachable",
            flops_identifier=flops_identifier,
            exception=ImageRegistryException,
            show_msg_on_success=True,
        ),
    )
    return True


# Note: (image) repos are the "grouping" of all tags of a single image.
# E.g. The (image) repo "alpine" can have multiple tags "latest", "1.0.0", etc.
# We usually first check the image repo and then its tags.
def get_current_registry_image_repos() -> List[str]:
    response = CustomRequest(
        core=RequestCore(
            base_url=ROOT_FL_IMAGE_REGISTRY_URL,
            api_endpoint="/v2/_catalog",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get current registry repositories",
            exception=ImageRegistryException,
        ),
    )
    return response["repositories"]


def get_current_registry_repo_image_tags(ml_repo: MlRepo) -> List[str]:
    response = CustomRequest(
        core=RequestCore(
            base_url=ROOT_FL_IMAGE_REGISTRY_URL,
            api_endpoint=f"/v2/{ml_repo.sanitized_name}/tags/list",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get image tags",
            exception=ImageRegistryException,
        ),
    )
    return response["tags"]


def fetch_latest_matching_image(ml_repo: MlRepo) -> Optional[str]:
    current_image_reqpositories = get_current_registry_image_repos()
    if ml_repo.sanitized_name not in current_image_reqpositories:
        return None

    current_image_tags = get_current_registry_repo_image_tags(ml_repo)
    latest_commit_hash = get_latest_commit_hash(ml_repo)
    return (
        f"{ml_repo.name}:{latest_commit_hash}" if latest_commit_hash in current_image_tags else None
    )
