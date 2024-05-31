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

    def __post_init__(self):
        global _context
        _context = self

    def trigger_build_plan(self) -> None:
        self.build_plan_trigger()


def get_context() -> Context:
    return _context
