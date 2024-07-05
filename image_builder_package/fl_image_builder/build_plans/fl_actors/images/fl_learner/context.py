from typing import List

from pydantic import BaseModel

_context = None


class LearnerContext(BaseModel):
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str

    aggregator_ip: str
    data_tags: List[str]

    def model_post_init(self, _) -> None:
        global _context
        _context = self


def get_context() -> LearnerContext:
    return _context  # type: ignore
