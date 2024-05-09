from abc import ABC, abstractmethod
from typing import ClassVar

from flops_manager.database.common import add_to_db
from flops_manager.utils.sla.components import SlaComponentsWrapper
from pydantic import BaseModel, Field


class FlOpsOakestraBaseClass(BaseModel, ABC):
    # TODO docs

    namespace: ClassVar[str]
    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return
        add_to_db(self)

    @abstractmethod
    def build_sla_components(self) -> SlaComponentsWrapper:
        pass
