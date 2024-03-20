from api.common import GITHUB_PREFIX
from github import Github

BUILDER_APP_NAMESPACE = "fl_build"


class MlRepo:
    def __init__(self, repo_url):
        self.url = repo_url
        self.name = repo_url.split(GITHUB_PREFIX)[-1]
        self.github_repo = Github().get_repo(self.name)
        self.latest_commit_hash = self.github_repo.get_commits()[0].sha[:7]
