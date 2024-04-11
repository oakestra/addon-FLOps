import os

# Note: Instead of using python-on-whales the more mature docker SDK python lib
# should not require/install the docker CLI to work.
import docker as docker_sdk

docker = docker_sdk.from_env()


# TODO figure out an automatic way to get the real public IP of the host (or another nicer solution)
FLOPS_IMAGE_REGISTRY_IP = "192.168.178.44"
FLOPS_IMAGE_REGISTRY_PORT = os.environ.get("FLOPS_IMAGE_REGISTRY_PORT")
FLOPS_IMAGE_REGISTRY_IP_WITH_PORT = f"{FLOPS_IMAGE_REGISTRY_IP}:{FLOPS_IMAGE_REGISTRY_PORT}"
FLOPS_IMAGE_REGISTRY_URL = f"https://{FLOPS_IMAGE_REGISTRY_IP_WITH_PORT}"
