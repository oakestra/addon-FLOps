from abc import ABC, abstractmethod
from typing import ClassVar, Optional

from flops_manager.database.common import add_to_db
from flops_manager.utils.sla.components import SlaComponentsWrapper
from pydantic import BaseModel, Field


class FlOpsOakestraBaseClass(BaseModel, ABC):
    namespace: ClassVar[str]
    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)
    sla_components: Optional[SlaComponentsWrapper] = Field(
        default=None,
        init=False,
        exclude=True,
        repr=False,
    )

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self._configure_sla_components()
        result = self._create_in_orchestrator()
        self._set_properties_based_on_created_result(result)
        add_to_db(self)

    @abstractmethod
    def _configure_sla_components(self) -> None:
        """Sets the self.sla_components property."""
        pass

    @abstractmethod
    def _create_in_orchestrator(self):
        pass

    def _set_properties_based_on_created_result(self, *_) -> None:
        pass
