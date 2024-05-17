from flops_manager.utils.types import CustomEnum


class Topics(CustomEnum):
    PROJECT_OBSERVER_FAILED = "flops_manager/project_observer/failed"
    IMAGE_BUILDER_SUCCESS = "flops_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "flops_manager/image_builder/failed"
    AGGREGATOR_SUCCESS = "flops_manager/aggregator/success"
    AGGREGATOR_FAILED = "flops_manager/aggregator/failed"
