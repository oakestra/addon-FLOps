from flops_manager.classes.oakestratables.deployables.base import DeployableClass
from pydantic import Field


class CustomerFacingComponent(DeployableClass):
    app_id: str = Field("", init=False)
    bearer_token: str = Field(exclude=True, repr=False)
