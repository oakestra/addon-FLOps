import os
import sys

from flops_utils.logging import logger

DOCKER_HOST_IP_LINUX = "172.17.0.1"

_ERROR_MESSAGE = (
    "Terminating. Make sure to set the environment variables first. Missing: "
)


def get_env_var(name: str, default: str = "") -> str:
    env_var = os.environ.get(name) or default
    if env_var is None:
        logger.fatal(f"{_ERROR_MESSAGE}'{name}'")
        sys.exit(1)
    return env_var
