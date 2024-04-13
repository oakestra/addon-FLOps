import github
from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.api.utils.consts import GITHUB_PREFIX
from flops_manager.classes.project_based import FlOpsProjectBasedClass
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from pydantic import Field


class MlRepo(FlOpsProjectBasedClass):
    url: str

    name: str = Field("", init=False)
    latest_commit_hash: str = Field("", init=False)
    sanitized_name: str = Field("", init=False, exclude=True)

    def model_post_init(self, _):
        self.name = self.url.split(GITHUB_PREFIX)[-1]
        self.latest_commit_hash = self.get_github_repo().get_commits()[0].sha[:7]
        self._add_to_db()

    def get_github_repo(self) -> github.Repository.Repository:
        return github.Github().get_repo(self.name)

    def get_sanitized_name(self) -> str:
        """The build FL image name will contain the github user + repo name for identification.
        The github user name might be uppercase, but docker image names (infix/prefix) cannot be."""
        if self.sanitized_name:
            return self.sanitized_name

        parts = self.name.split("/")
        parts[0] = parts[0].lower()
        self.sanitized_name = "/".join(parts)
        return self.sanitized_name

    def get_latest_commit_hash(self) -> str:
        response = CustomRequest(
            core=RequestCore(
                base_url="https://api.github.com",
                api_endpoint=f"/repos/{self.get_sanitized_name()}/commits/main",
            ),
            aux=RequestAuxiliaries(
                what_should_happen="Fetch commits from github",
                flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
                is_oakestra_api=False,
            ),
        ).execute()
        return response["sha"]
