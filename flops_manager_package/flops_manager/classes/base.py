from abc import ABC

from pydantic import BaseModel, Field


class FlOpsBaseClass(BaseModel, ABC):
    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)
