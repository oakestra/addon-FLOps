from dataclasses import dataclass, field

import github
from api.consts import GITHUB_PREFIX
from database.main import DbCollections
from utils.classes.base import FlOpsBaseClass

BUILDER_APP_NAMESPACE = "flbuild"


@dataclass
class MlRepo(FlOpsBaseClass):
    flops_process_id: str
    url: str

    name: str = field(init=False)
    sanitized_name: str = field(init=False)
    latest_commit_hash: str = field(init=False)

    def __post_init__(self):
        self.db_collection_type = DbCollections.ML_REPOS
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
