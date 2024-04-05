from api.consts import GITHUB_PREFIX
from github import Github

BUILDER_APP_NAMESPACE = "flbuild"


class MlRepo:
    def __init__(self, repo_url):
        self.url = repo_url
        self.name = repo_url.split(GITHUB_PREFIX)[-1]
        # Note: The build FL image name will contain the github user + repo name for identification.
        # The github user name might be uppercase, but docker image names (infix/prefix) cannot be.
        parts = self.name.split("/")
        parts[0] = parts[0].lower()
        self.sanitized_name = "/".join(parts)
        self.github_repo = Github().get_repo(self.name)
        self.latest_commit_hash = self.github_repo.get_commits()[0].sha[:7]
