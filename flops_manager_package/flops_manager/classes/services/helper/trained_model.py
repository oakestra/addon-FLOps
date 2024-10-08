from typing import Optional

from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.utils.common import generate_ip, get_shortened_unique_id
from flops_manager.utils.env_vars import TRAINED_MODEL_PORT
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import Field


class TrainedModel(FLOpsService):
    namespace = "trmodel"
    parent_app: Optional[FLOpsHelperApp] = Field(default=None, exclude=True, repr=False)
    image_name: str = ""

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.ip = generate_ip(self.parent_app.app_id, self)  # type: ignore
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        parent_app_id = self.parent_app.app_id  # type: ignore
        service_name = f"{self.namespace}{get_shortened_unique_id(parent_app_id)}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.parent_app.customer_id,  # type: ignore
                app_id=parent_app_id,
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(code=self.image_name),
            ),
            details=SlaDetails(
                # TODO: Need adjusting
                resources=SlaResources(memory=200, vcpus=1, storage=0),
                port=str(TRAINED_MODEL_PORT),
            ),
        )
