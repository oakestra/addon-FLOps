from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

import git
from build_plans.fl_actors.dependency_management.main import handle_dependencies
from build_plans.fl_actors.paths import CLONED_REPO_PATH, CONDA_ENV_FILE_PATH, FL_BASE_IMAGE_PATH
from flops_utils.shell import run_in_shell

if TYPE_CHECKING:
    from context.main import Context


def clone_repo(context: Context) -> None:
    repo_url = context.repo_url
    try:
        repo = git.Repo.clone_from(repo_url, str(CLONED_REPO_PATH))
    except Exception as e:
        context.notify_about_failed_build_and_terminate(f"Failed to clone repo '{repo_url}'; '{e}'")

    context.set_cloned_repo(repo)


def _normalize_conda_env_name() -> None:
    run_in_shell(f"sed -i -e 's/name: .*/name: base/' {CONDA_ENV_FILE_PATH}")


def _copy_verified_repo_content_into_fl_base_image() -> None:
    for item in CLONED_REPO_PATH.iterdir():
        src = item
        dst = FL_BASE_IMAGE_PATH / item.name
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)


# NOTE: Further checks can be added here, e.g.:
# - if the conda dependencies make sense, are valid
# - maybe even "adjust/augment" them here
# - check if any malicious code is included in this repo
# -- to avoid running this code in on the worker node.
def check_cloned_repo(context: Context) -> None:
    cloned_repo = context.cloned_repo
    root_tree = cloned_repo.tree()

    files_to_check = ["model_manager.py", CONDA_ENV_FILE_PATH.name]
    for file in files_to_check:
        if file not in [blob.name for blob in root_tree.blobs]:
            context.notify_about_failed_build_and_terminate(
                f"{file} not found in the cloned repository."
            )

    _normalize_conda_env_name()
    handle_dependencies()
    _copy_verified_repo_content_into_fl_base_image()
