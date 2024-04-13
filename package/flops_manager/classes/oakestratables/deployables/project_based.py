from abc import ABC

from flops_manager.classes.oakestratables.deployables.base import DeployableClass
from flops_manager.classes.oakestratables.project_based import FlOpsOakestraProjectBasedClass


class DeployableProjectBasedClass(DeployableClass, FlOpsOakestraProjectBasedClass, ABC):
    pass
