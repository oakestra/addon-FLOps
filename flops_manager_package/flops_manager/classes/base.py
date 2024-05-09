from abc import ABC, abstractmethod
from typing import ClassVar

from flops_manager.database.common import add_to_db
from flops_manager.utils.sla.components import SlaComponentsWrapper
from pydantic import BaseModel, Field


class FlOpsOakestraBaseClass(BaseModel, ABC):
    # TODO docs

    # Note:
    # This "Field"s help to make the constructor call for human developers easier to read.
    # It removes fields that should not be explicitly displayed in the IDE hints.
    # This does not break loading/reinstantiating the object when fetching it from the DB.
    #
    # The only downside is that it still requires a set value during the constructor call.
    # The current workaround is to set a dummy default value.
    # The potential issue here is that if this field is not set correctly during the construction,
    # this object will still count as valid, which it is not.
    #
    # TODO add a "post init" (custom) validator to check
    # if all properties are properly set and not empty/""
    namespace: ClassVar[str]
    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)

    # Note: This attribute is only used during object construction.
    # It is not stored or displayed due to verbosity & redundancy.
    sla_components: SlaComponentsWrapper = Field(None, init=False, exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self._configure_sla_components()
        add_to_db(self)

    @abstractmethod
    def _configure_sla_components(self) -> None:
        """Sets self.sla_components that are needed for deployments"""
        pass
