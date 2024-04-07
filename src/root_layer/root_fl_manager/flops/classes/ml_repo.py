import github
from api.utils.consts import GITHUB_PREFIX
from flops.classes.abstract.base import FlOpsBaseClass
from pydantic import Field


class MlRepo(FlOpsBaseClass):
    url: str

    name: str = Field("", init=False)
    sanitized_name: str = Field("", init=False)
    latest_commit_hash: str = Field("", init=False)

    def model_post_init(self, _):
        self.name = self.url.split(GITHUB_PREFIX)[-1]
        # Note: The build FL image name will contain the github user + repo name for identification.
        # The github user name might be uppercase, but docker image names (infix/prefix) cannot be.
        parts = self.name.split("/")
        parts[0] = parts[0].lower()
        self.sanitized_name = "/".join(parts)
        self.latest_commit_hash = self.get_github_repo().get_commits()[0].sha[:7]
        self._add_to_db()

    def get_github_repo(self) -> github.Repository.Repository:
        return github.Github().get_repo(self.name)
