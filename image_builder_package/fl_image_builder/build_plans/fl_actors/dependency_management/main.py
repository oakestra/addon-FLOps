from build_plans.fl_actors.dependency_management.pytorch import handle_pytorch
from build_plans.fl_actors.paths import CONDA_ENV_FILE_PATH
from flops_utils.shell import run_in_shell


def dependency_exists(target_dependency: str) -> bool:
    shell_cmd = f"grep '{target_dependency}' {CONDA_ENV_FILE_PATH}"
    # Hint: success = returncode == 0 -> bool = false
    #       failure = returncode != 0 -> bool = true
    # -> needs to be inverted
    return not bool(run_in_shell(shell_cmd, check=False).returncode)


def remove_mlflow() -> None:
    """There does not seem to be a reason to have mlflow as a dependency for the learner.
    In addition mlflow can be used to track what clients/learners are doing
    which violates the security promises made by FL.
    MLflow is a great tool to extract the necessary dependencies of ML code though.
    MLflow is used in the aggregator. Where the dependency is added again with a fixed version.
    """
    run_in_shell(f"sed -i '/ - mlflow/d' {CONDA_ENV_FILE_PATH}")


def handle_dependencies():
    remove_mlflow()
    handle_pytorch()
