from api.request_management.custom_requests import CustomRequest, RequestAuxiliaries, RequestCore
from flops.classes.ml_repo import MlRepo
from utils.classes.exceptions import ImageRegistryException


def get_latest_commit_hash(ml_repo: MlRepo) -> str:
    response = CustomRequest(
        core=RequestCore(
            base_url="https://api.github.com",
            api_endpoint=f"/repos/{ml_repo.get_sanitized_name()}/commits/main",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Fetch commits from github",
            exception=ImageRegistryException,
            is_oakestra_api=False,
        ),
    ).execute()
    return response["sha"]
