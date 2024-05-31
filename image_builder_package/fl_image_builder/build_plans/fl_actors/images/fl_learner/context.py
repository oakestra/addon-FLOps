from typing import List

from pydantic import BaseModel

_context = None


class LearnerContext(BaseModel):
    aggregator_ip: str
    data_tags: List[str]

    def model_post_init(self, _) -> None:
        global _context
        _context = self


def get_context() -> LearnerContext:
    return _context
