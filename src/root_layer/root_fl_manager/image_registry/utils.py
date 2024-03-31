from http import HTTPStatus
from typing import Optional, Tuple

from api.utils import handle_request
from image_builder_management.common import MlRepo


def get_latest_commit_hash(ml_repo: MlRepo) -> Tuple[HTTPStatus, Optional[str]]:
    git_api_endpoint = f"/repos/{ml_repo.sanitized_name}/commits/main"
    status, json_data = handle_request(
        base_url="https://api.github.com",
        what_should_happen="Fetch commits from github",
        api_endpoint=git_api_endpoint,
        is_oakestra_api=False,
    )
    if status != HTTPStatus.OK:
        return status, None

    return status, json_data["sha"]
