from flops_manager.utils.types import CustomEnum


class Topics(CustomEnum):
    PROJECT_OBSERVER_FAILED = "flops_manager/project_observer/failed"

    FL_ACTORS_IMAGE_BUILDER_SUCCESS = "flops_manager/fl_actors_image_builder/success"
    FL_ACTORS_IMAGE_BUILDER_FAILED = "flops_manager/fl_actors_image_builder/failed"

    TRAINED_MODEL_IMAGE_BUILDER_SUCCESS = "flops_manager/trained_model_image_builder/success"
    TRAINED_MODEL_IMAGE_BUILDER_FAILED = "flops_manager/trained_model_image_builder/failed"

    AGGREGATOR_SUCCESS = "flops_manager/aggregator/success"
    AGGREGATOR_FAILED = "flops_manager/aggregator/failed"
