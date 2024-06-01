from dataclasses import dataclass

from build_plans.trained_model.main import handle_trained_model_image_build
from context.main import Context


@dataclass
class ContextTrainedModel(Context):
    build_plan_trigger = handle_trained_model_image_build
    mqtt_topic_infix = "trained_model_image_builder"

    customer_id: str
    tracking_server_uri: str
    run_id: str
