from http import HTTPStatus
from typing import List, Optional, Tuple

from api.utils import handle_request
from image_builder_management.common import MlRepo
from image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from image_registry.utils import get_latest_commit_hash


def check_registry_reachable() -> HTTPStatus:
    status, _ = handle_request(
        base_url=ROOT_FL_IMAGE_REGISTRY_URL,
        what_should_happen="Registry is reachable",
    )
    return status


# Note: (image) repos are the "grouping" of all tags of a single image.
# E.g. The (image) repo "alpine" can have multiple tags "latest", "1.0.0", etc.
# We usually first check the image repo and then its tags.
def get_current_registry_image_repos() -> Tuple[HTTPStatus, Optional[List[str]]]:
    status, json_data = handle_request(
        base_url=ROOT_FL_IMAGE_REGISTRY_URL,
        api_endpoint="/v2/_catalog",
        what_should_happen="Get current registry repositories",
    )
    if status != HTTPStatus.OK:
        return status, None
    return status, json_data["repositories"]


def get_current_registry_repo_image_tags(ml_repo: MlRepo) -> Tuple[HTTPStatus, Optional[List[str]]]:
    status, json_data = handle_request(
        base_url=ROOT_FL_IMAGE_REGISTRY_URL,
        api_endpoint=f"/v2/{ml_repo.name}/tags/list",
        what_should_happen="Get image tags",
    )
    if status != HTTPStatus.OK:
        return status, None
    return status, json_data["tags"]


def fetch_latest_matching_image(ml_repo: MlRepo) -> Tuple[HTTPStatus, Optional[str]]:
    status, current_images_repos = get_current_registry_image_repos()

    if status != HTTPStatus.OK or ml_repo.name not in current_images_repos:
        return status, None

    status, current_image_repo_tags = get_current_registry_repo_image_tags(ml_repo)
    if status != HTTPStatus.OK:
        return status, None
    status, latest_commit_hash = get_latest_commit_hash(ml_repo)

    if status != HTTPStatus.OK:
        return status, None

    if latest_commit_hash in current_image_repo_tags:
        return status, f"{ml_repo.name}:{latest_commit_hash}"
    else:
        return status, None
