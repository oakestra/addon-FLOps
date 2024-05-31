from dataclasses import dataclass, field

import git
from build_plans.fl_actors import build_fl_actor_images
from context.main import Context
from flops_utils.types import MLModelFlavor


@dataclass
class ContextFLActors(Context):
    build_plan_trigger = build_fl_actor_images

    ml_model_flavor: MLModelFlavor
    repo_url: str
    use_devel_base_images: bool = False

    cloned_repo: git.repo.base.Repo = field(default=None, init=False)
    new_image_name_prefix: str = field(default="", init=False)
    new_image_tag: str = field(default="", init=False)

    def set_cloned_repo(self, cloned_repo: git.repo.base.Repo) -> None:
        self.cloned_repo = cloned_repo

    def set_new_image_name_prefix(self, new_image_name_prefix: str) -> None:
        self.new_image_name_prefix = new_image_name_prefix

    def set_new_image_tag(self, new_image_tag: str) -> None:
        self.new_image_tag = new_image_tag

    def _build_image_name(self, infix: str) -> str:
        return f"{self.new_image_name_prefix}/{infix}:{self.new_image_tag}"

    def get_learner_image_name(self) -> str:
        return self._build_image_name("learner")

    def get_aggregator_image_name(self) -> str:
        return self._build_image_name("aggregator")
