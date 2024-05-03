import shutil

import git
from dependency_management.main import handle_dependencies
from notification_management import notify_about_failed_build_and_terminate
from utils.build_context import get_build_context
from utils.common import (
    CLONED_REPO_PATH,
    CONDA_ENV_FILE_PATH,
    FL_BASE_IMAGE_PATH,
    run_in_bash,
)


def clone_repo() -> None:
    repo_url = get_build_context().repo_url
    try:
        repo = git.Repo.clone_from(repo_url, str(CLONED_REPO_PATH))
    except Exception as e:
        notify_about_failed_build_and_terminate(
            f"Failed to clone repo '{repo_url}'; '{e}'"
        )

    get_build_context().set_cloned_repo(repo)


def _normalize_conda_env_name() -> None:
    run_in_bash(f"sed -i -e 's/name: .*/name: base/' {CONDA_ENV_FILE_PATH}")


def _copy_verified_repo_content_into_fl_base_image() -> None:
    for item in CLONED_REPO_PATH.iterdir():
        src = item
        dst = FL_BASE_IMAGE_PATH / item.name
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)


# Note: Further checks can be added here, e.g.:
# - if the conda dependencies make sense, are valid
# - maybe even "adjust/augment" them here
# - check if any maliciouse code is included in this repo
# -- to avoid running this code in on the worker node.
def check_cloned_repo() -> None:
    cloned_repo = get_build_context().cloned_repo
    root_tree = cloned_repo.tree()

    files_to_check = ["model_manager.py", CONDA_ENV_FILE_PATH.name]
    for file in files_to_check:
        if file not in [blob.name for blob in root_tree.blobs]:
            notify_about_failed_build_and_terminate(
                f"{file} not found in the cloned repository."
            )

    _normalize_conda_env_name()
    handle_dependencies()
    _copy_verified_repo_content_into_fl_base_image()
