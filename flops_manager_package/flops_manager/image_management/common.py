from flops_manager.registry_management import FLOPS_IMAGE_REGISTRY_IP, FLOPS_IMAGE_REGISTRY_PORT


def get_flops_image_prefix() -> str:
    return f"{FLOPS_IMAGE_REGISTRY_IP}:{FLOPS_IMAGE_REGISTRY_PORT}/"
