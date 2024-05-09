from abc import ABC

from pydantic import BaseModel, Field


class FlOpsProjectBasedClass(BaseModel, ABC):
    flops_project_id: str
    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)
