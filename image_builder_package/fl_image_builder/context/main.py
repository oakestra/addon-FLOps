import abc
from dataclasses import dataclass, field

from flops_utils.timer import Timer

_context = None


@dataclass
class Context(abc.ABC):
    image_registry_url: str
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    deactivate_notifications: bool
    timer: Timer = field(default_factory=Timer, init=False)

    def __post_init__(self):
        global _context
        _context = self


def get_context() -> Context:
    return _context
