import build_plans.fl_actors.dependency_management.main as dep_manager
from build_plans.fl_actors.paths import CONDA_ENV_FILE_PATH
from flops_utils.shell import run_in_shell


def _handle_pyvision() -> None:
    if not dep_manager.dependency_exists("pyvision") and dep_manager.dependency_exists("gmpy2"):
        run_in_shell(f"sed -i 's/- gmpy2.*/- torchvision/' {CONDA_ENV_FILE_PATH}")


def handle_pytorch():
    if dep_manager.dependency_exists("torch"):
        _handle_pyvision()
