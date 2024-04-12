from flops_manager.classes.oakestratables.deployables.base import DeployableClass
from pydantic import Field


class CustomerFacingComponent(DeployableClass):
    bearer_token: str = Field(exclude=True, repr=False)

    app_id: str = Field("", init=False)
