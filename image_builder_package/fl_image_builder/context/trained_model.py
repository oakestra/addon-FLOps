from dataclasses import dataclass

from build_plans.trained_model.main import handle_trained_model_image_build
from context.main import Context
from flops_utils.mqtt_topics import Subject


@dataclass
class ContextTrainedModel(Context):
    build_plan_trigger = handle_trained_model_image_build
    mqtt_subject = Subject.TRAINED_MODEL_IMAGE_BUILDER

    customer_id: str
    tracking_server_uri: str
    run_id: str
