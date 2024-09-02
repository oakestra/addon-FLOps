# NOTE: Even for the trained_model build-plan we need to check if the dependencies are correct.
# E.g. the simplest pytorch example is able to be build and trained but for the trained model
# mlflow extracts a new dependency file with broken dependencies!

import pathlib

from flops_utils.shell import run_in_shell

REQUIREMENTS_FILE = pathlib.Path(
    "/image_builder/trained_model_dockerfile_dir/model_dir/logged_model_artifact/requirements.txt"
)


def dependency_exists(target_dependency: str) -> bool:
    shell_cmd = f"grep '{target_dependency}' {REQUIREMENTS_FILE}"
    # Hint: success = returncode == 0 -> bool = false
    #       failure = returncode != 0 -> bool = true
    # -> needs to be inverted
    return not bool(run_in_shell(shell_cmd, check=False).returncode)


def handle_dependencies():
    _handle_pyarrow()


def _handle_pyarrow():
    if dependency_exists("mlflow==2.14.3") and dependency_exists("pyarrow==17.0.0"):
        pattern = r"s/pyarrow==17\.0\.0/pyarrow==15\.0\.0/g"
        run_in_shell(f"sed -i '{pattern}' {REQUIREMENTS_FILE}")
