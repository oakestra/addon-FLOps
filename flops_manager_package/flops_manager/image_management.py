from typing import List

from flops_manager.ml_repo_management import get_sanitize_ml_repo_name
from flops_manager.registry_management import (
    FLOPS_IMAGE_REGISTRY_IP,
    FLOPS_IMAGE_REGISTRY_PORT,
    get_current_registry_image_repo_names,
    get_current_tags_for_image_in_registry,
)
from flops_manager.utils.types import CustomEnum


class FLOpsImageTypes(CustomEnum):
    LEARNER = "learner"
    AGGREGATOR = "aggregator"


def get_expected_image_repo_names_for_project(ml_repo_url: str) -> List[str]:
    sanitized_image_repo_name = get_sanitize_ml_repo_name(ml_repo_url)
    expected_image_repo_names = []
    for flops_image_type in FLOpsImageTypes:
        expected_image_repo_names.append(f"{sanitized_image_repo_name}/{flops_image_type}")
    return expected_image_repo_names


def check_if_latest_matching_images_exist(
    ml_repo_url: str,
    ml_repo_latest_commit_hash: str,
) -> bool:
    current_image_repo_names = get_current_registry_image_repo_names()
    expected_image_repo_names = get_expected_image_repo_names_for_project(ml_repo_url)
    if not all(
        image_repo_name in current_image_repo_names for image_repo_name in expected_image_repo_names
    ):
        return False

    for image_repo_name in expected_image_repo_names:
        current_matching_image_tags_in_registry = get_current_tags_for_image_in_registry(
            image_repo_name
        )
        if ml_repo_latest_commit_hash not in current_matching_image_tags_in_registry:
            return False

    return True


def get_flops_image_name(
    ml_repo_url: str,
    ml_repo_latest_commit_hash: str,
    flops_image_type: FLOpsImageTypes,
) -> str:
    return "".join(
        (
            FLOPS_IMAGE_REGISTRY_IP,
            ":",
            FLOPS_IMAGE_REGISTRY_PORT,
            "/",
            get_sanitize_ml_repo_name(ml_repo_url),
            "/",
            flops_image_type.value,
            ":",
            ml_repo_latest_commit_hash,
        )
    )
