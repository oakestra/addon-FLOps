from dataclasses import dataclass, field

import git
from flops_utils.timer import Timer
from flops_utils.types import MLModelFlavor

_build_context = None

FULL_BUILDER_PROCESS_TIMEFRAME = "full_builder_process"
BUILD_PREPARATION_TIMEFRAME = "build_preparation"
BUILD_ALL_IMAGES_TIMEFRAME = "build_all_images"
BASE_IMAGE_BUILD_TIMEFRAME = "base_image_build"
IMAGE_PUSH_TIMEFRAME = "image_push"


@dataclass
class BuilderContext:
    ml_model_flavor: MLModelFlavor
    repo_url: str
    image_registry_url: str
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    develop: bool = False

    cloned_repo: git.repo.base.Repo = field(default=None, init=False)
    new_image_name_prefix: str = field(default="", init=False)
    new_image_tag: str = field(default="", init=False)

    timer: Timer = field(default_factory=Timer, init=False)

    def __post_init__(self):
        global _build_context
        _build_context = self

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


def get_builder_context() -> BuilderContext:
    return _build_context
