import os
import sys
from typing import Union

from flops_utils.logging import logger

ERROR_MESSAGE = (
    "Terminating Flops Manager. Make sure to set the environment variables first. Missing: "
)


def _get_env_var(name: str, default: Union[str, int] = None) -> str:
    env_var = os.environ.get(name) or default
    if env_var is None:
        logger.fatal(f"{ERROR_MESSAGE}'{name}'")
        sys.exit(1)
    return env_var


SYSTEM_MANAGER_IP = _get_env_var("SYSTEM_MANAGER_IP")
SYSTEM_MANAGER_PORT = _get_env_var("SYSTEM_MANAGER_PORT", 1000)

FLOPS_MANAGER_IP = _get_env_var("FLOPS_MANAGER_IP")
FLOPS_MANAGER_PORT = _get_env_var("FLOPS_MANAGER_PORT", 5072)
FLOPS_DB_PORT = _get_env_var("FLOPS_DB_PORT", 10027)

FLOPS_MQTT_BROKER_IP = _get_env_var("FLOPS_MQTT_BROKER_IP")
FLOPS_MQTT_BROKER_PORT = _get_env_var("FLOPS_MQTT_BROKER_PORT", 9027)

FLOPS_IMAGE_REGISTRY_IP = _get_env_var("FLOPS_IMAGE_REGISTRY_IP")
ARTIFACT_STORE_IP = _get_env_var("ARTIFACT_STORE_IP")
BACKEND_STORE_IP = _get_env_var("BACKEND_STORE_IP")
