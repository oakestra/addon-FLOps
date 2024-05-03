import pathlib
import shlex
import subprocess

IMAGES_PATH = pathlib.Path("images")
FL_BASE_IMAGE_PATH = IMAGES_PATH / "fl_base"
FL_LEARNER_IMAGE_PATH = IMAGES_PATH / "fl_learner"
FL_AGGREGATOR_IMAGE_PATH = IMAGES_PATH / "fl_aggregator"

CLONED_REPO_PATH = pathlib.Path("/tmp") / "cloned_repo"
CONDA_ENV_FILE_PATH = CLONED_REPO_PATH / "conda.yaml"


def run_in_bash(bash_cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(shlex.split(bash_cmd), capture_output=True)
