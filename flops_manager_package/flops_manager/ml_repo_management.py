import github
from flops_manager.api.utils.consts import GITHUB_PREFIX
from pydantic import BaseModel, Field


class MLRepoInfo(BaseModel):
    url: str
    latest_commit_hash: str = Field("", init=False)

    def model_post_init(self, _):
        self.latest_commit_hash = get_latest_commit_hash(self.url)


def _get_ml_repo_name(ml_repo_url: str) -> str:
    return ml_repo_url.split(GITHUB_PREFIX)[-1]


def _get_github_repo(repo_name: str) -> github.Repository.Repository:
    return github.Github().get_repo(repo_name)


def get_latest_commit_hash(ml_repo_url: str) -> str:
    return _get_github_repo(repo_name=_get_ml_repo_name(ml_repo_url)).get_commits()[0].sha


def get_sanitize_ml_repo_name(ml_repo_url: str) -> str:
    """The build FL image name will contain the github user + repo name for identification.
    The github user name might be uppercase, but docker image names (infix/prefix) cannot be."""
    parts = _get_ml_repo_name(ml_repo_url).split("/")
    parts[0] = parts[0].lower()
    return "/".join(parts)
