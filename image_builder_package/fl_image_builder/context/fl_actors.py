from dataclasses import dataclass, field

import git
from build_plans.fl_actors.main import handle_fl_actor_images_build
from context.main import Context
from flops_utils.types import MLModelFlavor


@dataclass
class ContextFLActors(Context):
    build_plan_trigger = handle_fl_actor_images_build
    mqtt_topic_infix = "fl_actors_image_builder"

    ml_model_flavor: MLModelFlavor
    repo_url: str
    use_devel_base_images: bool = False

    cloned_repo: git.repo.base.Repo = field(default=None, init=False)

    def set_cloned_repo(self, cloned_repo: git.repo.base.Repo) -> None:
        self.cloned_repo = cloned_repo

    def get_learner_image_name(self) -> str:
        return self._build_image_name("learner")

    def get_aggregator_image_name(self) -> str:
        return self._build_image_name("aggregator")
