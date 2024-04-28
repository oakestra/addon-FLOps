from typing import List, Optional

from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.classes.ml_repo import MlRepo
from flops_manager.classes.oak.project import FlOpsProject
from flops_manager.image_registry_management.common import (
    FLOPS_IMAGE_REGISTRY_IP,
    FLOPS_IMAGE_REGISTRY_PORT,
    FLOPS_IMAGE_REGISTRY_URL,
)
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_manager.utils.types import FLOpsImageType
from icecream import ic


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


def _get_current_registry_repo_image_tag(image_repo_name: str) -> List[str]:
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


def get_current_registry_repo_image_tag(ml_repo: MlRepo) -> str:
    matching_learner_image_tags = (
        _get_current_registry_repo_image_tag(ml_repo.get_image_name(FLOpsImageType.LEARNER)),
    )
    matching_aggregator_image_tags = (
        _get_current_registry_repo_image_tag(ml_repo.get_image_name(FLOpsImageType.AGGREGATOR)),
    )

    if matching_learner_image_tags == matching_aggregator_image_tags:
        # Note: The tags are based on the latest ML repo commit hash.
        # Thus the image tags for the Learner and Aggregator are the same.
        return matching_learner_image_tags

    raise FLOpsManagerException(
        flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        mgs=" ".join(
            (
                "Found image tags do not match!",
                f"Learner tags = '{matching_learner_image_tags}'",
                f"Aggregator tags = '{matching_aggregator_image_tags}'",
            )
        ),
        flops_project_id=ml_repo.flops_project_id,
    )


def check_if_latest_matching_images_exists(ml_repo: MlRepo) -> bool:
    current_image_repositories = get_current_registry_image_repos()

    if not all(
        image in current_image_repositories
        for image in [
            ml_repo.get_image_name(FLOpsImageType.LEARNER),
            ml_repo.get_image_name(FLOpsImageType.AGGREGATOR),
        ]
    ):
        return False

    current_image_tag = get_current_registry_repo_image_tag(ml_repo)
    latest_commit_hash = ml_repo.get_latest_commit_hash()

    full_image_reference = "".join(
        (
            FLOPS_IMAGE_REGISTRY_IP,
            ":",
            FLOPS_IMAGE_REGISTRY_PORT,
            "/",
            ml_repo.get_sanitized_name(),
            ":",
            latest_commit_hash,
        )
    )
    return full_image_reference if latest_commit_hash in current_image_tags else None
