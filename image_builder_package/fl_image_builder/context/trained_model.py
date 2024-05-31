from dataclasses import dataclass

from build_plans.trained_model import build_trained_model_image
from context.main import Context


@dataclass
class ContextTrainedModel(Context):
    build_plan_trigger = build_trained_model_image

    run_id: str
