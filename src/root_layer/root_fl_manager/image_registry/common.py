import os

# Note: Instead of using python-on-whales the more mature docker SDK python lib
# should not require/install the docker CLI to work.
import docker as docker_sdk

docker = docker_sdk.from_env()


# TODO figure out an automatic way to get the real public IP of the host (or another nicer solution)
ROOT_FL_IMAGE_REGISTRY_NAME = "192.168.178.44"
ROOT_FL_IMAGE_REGISTRY_PORT = os.environ.get("ROOT_FL_IMAGE_REGISTRY_PORT")
FULL_ROOT_FL_IMAGE_REGISTRY_NAME = f"{ROOT_FL_IMAGE_REGISTRY_NAME}:{ROOT_FL_IMAGE_REGISTRY_PORT}"
ROOT_FL_IMAGE_REGISTRY_URL = f"https://{FULL_ROOT_FL_IMAGE_REGISTRY_NAME}"
