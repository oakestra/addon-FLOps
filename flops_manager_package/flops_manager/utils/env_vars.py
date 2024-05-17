import os
import sys

from flops_utils.logging import logger

SYSTEM_MANAGER_IP = os.environ.get("SYSTEM_MANAGER_IP")
SYSTEM_MANAGER_PORT = os.environ.get("SYSTEM_MANAGER_PORT")

FLOPS_MANAGER_IP = os.environ.get("FLOPS_MANAGER_IP")
FLOPS_MANAGER_PORT = os.environ.get("FLOPS_MANAGER_PORT")
FLOPS_DB_PORT = os.environ.get("FLOPS_DB_PORT")

FLOPS_MQTT_BROKER_IP = os.environ.get("FLOPS_MQTT_BROKER_IP")
FLOPS_MQTT_BROKER_PORT = os.environ.get("FLOPS_MQTT_BROKER_PORT")

FLOPS_IMAGE_REGISTRY_IP = os.environ.get("FLOPS_IMAGE_REGISTRY_IP")
ARTIFACT_STORE_IP = os.environ.get("ARTIFACT_STORE_IP")
BACKEND_STORE_IP = os.environ.get("BACKEND_STORE_IP")


ERROR_MESSAGE = (
    "Terminating Flops Manager. Make sure to set the environment variables first. Missing: "
)


def check_if_env_vars_are_set() -> None:
    env_vars = [
        SYSTEM_MANAGER_IP,
        SYSTEM_MANAGER_PORT,
        FLOPS_MANAGER_IP,
        FLOPS_MANAGER_PORT,
        FLOPS_DB_PORT,
        FLOPS_MQTT_BROKER_IP,
        FLOPS_MQTT_BROKER_PORT,
        FLOPS_IMAGE_REGISTRY_IP,
        ARTIFACT_STORE_IP,
        BACKEND_STORE_IP,
    ]
    for var in env_vars:
        if var is None:
            logger.fatal(f"{ERROR_MESSAGE}'{var.}'")
            sys.exit(1)
