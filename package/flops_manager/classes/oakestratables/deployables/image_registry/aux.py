from flops_manager.classes.oakestratables.deployables.image_registry.main import FLOpsImageRegistry

_flops_image_builder = None


def init_flops_image_registry() -> FLOpsImageRegistry:
    global _flops_image_builder
    _flops_image_builder = FLOpsImageRegistry()
    return _flops_image_builder


def get_flops_image_registry() -> FLOpsImageRegistry:
    if not _flops_image_builder:
        return init_flops_image_registry()
    return _flops_image_builder
