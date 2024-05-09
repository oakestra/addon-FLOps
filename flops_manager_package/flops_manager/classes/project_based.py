from abc import ABC

from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.base import FlOpsOakestraBaseClass
from pydantic import Field


class FlOpsOakestraProjectBasedClass(FlOpsOakestraBaseClass, ABC):
    """A base class used for components that are based on a FLOps Project"""

    # Note: Use the entire Project object instead but only store & display its id.
    flops_project: FLOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)
