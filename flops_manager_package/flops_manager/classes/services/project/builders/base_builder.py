import abc

from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.registry_management import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from flops_utils.logging import logger
from pydantic import Field


class FLOpsBaseImageBuilder(FLOpsProjectService, abc.ABC):
    namespace = "builder"
    project_observer_ip: str = Field(default="", exclude=True, repr=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="New FLOps images need to be build. Start build delegation processes.",
            )

        super().model_post_init(_)

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="New Builder service created & deployed",
            )

    def _prepare_cmd(self) -> str:
        return " ".join(
            (
                "python3",
                "main.py",
                FLOPS_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,  # type: ignore
            )
        )

    def _configure_sla_components(self) -> None:
        parent_app_id = self.parent_app.app_id  # type: ignore
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=f"builder{get_shortened_unique_id(parent_app_id)}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-image-builder:latest",
                    one_shot_service=True,
                    cmd=self._prepare_cmd(),
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(
                    memory=2000,
                    vcpus=1,
                    storage=15000,
                ),
                privileged=True,
            ),
        )

    @classmethod
    def handle_builder_failed(cls, builder_failed_msg: dict) -> None:
        logger.debug(builder_failed_msg)
        flops_project_id = builder_failed_msg["flops_project_id"]
        retrieve_from_db_by_project_id(cls, flops_project_id).undeploy()  # type: ignore
        msg = "Builder failed. Terminating this FLOps Project."
        logger.critical(msg)
        notify_project_observer(flops_project_id=flops_project_id, msg=msg)

    @classmethod
    def handle_builder_success(cls, builder_success_msg: dict) -> str:
        """Undeploys the builder service and returns its FLOps Project ID."""
        logger.debug(builder_success_msg)
        flops_project_id = builder_success_msg["flops_project_id"]
        builder = retrieve_from_db_by_project_id(cls, flops_project_id)
        builder.undeploy()  # type: ignore
        return flops_project_id
