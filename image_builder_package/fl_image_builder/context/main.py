import abc
from dataclasses import dataclass, field
from typing import ClassVar

from flops_utils.timer import Timer

_context = None


@dataclass
class Context(abc.ABC):
    build_plan_trigger: ClassVar[callable]

    image_registry_url: str
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    deactivate_notifications: bool
    timer: Timer = field(default_factory=Timer, init=False)
    new_image_name_prefix: str = field(default="", init=False)
    new_image_tag: str = field(default="", init=False)

    def __post_init__(self):
        global _context
        _context = self

    def trigger_build_plan(self) -> None:
        self.build_plan_trigger()

    def set_new_image_name_prefix(self, new_image_name_prefix: str) -> None:
        self.new_image_name_prefix = new_image_name_prefix

    def set_new_image_tag(self, new_image_tag: str) -> None:
        self.new_image_tag = new_image_tag

    def _build_image_name(self, infix: str = None) -> str:
        if infix:
            return f"{self.new_image_name_prefix}/{infix}:{self.new_image_tag}"
        else:
            return f"{self.new_image_name_prefix}:{self.new_image_tag}"

    def get_image_name(self) -> str:
        return self._build_image_name()


def get_context() -> Context:
    return _context
