import os
import sys
from typing import Union

from flops_utils.logging import logger

ERROR_MESSAGE = (
    "Terminating. Make sure to set the environment variables first. Missing: "
)


def get_env_var(name: str, default: Union[str, int] = None) -> str:
    env_var = os.environ.get(name) or default
    if env_var is None:
        logger.fatal(f"{ERROR_MESSAGE}'{name}'")
        sys.exit(1)
    return env_var
