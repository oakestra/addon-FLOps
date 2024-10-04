import abc

from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.registry_management import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
from flops_manager.utils.sla.components import (
    IMAGE_BUILDER_ADDON_TYPE,
    AddonConstraint,
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

        assert self.parent_app
        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="New FLOps images need to be build. Start build delegation processes.",
            )

        super().model_post_init(_)

        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="New Builder service created & deployed",
            )

    def _prepare_cmd(self) -> str:
        assert self.parent_app
        supported_platforms = ",".join(
            [platform.value for platform in self.parent_app.supported_platforms]
        )
        return " ".join(
            (
                "python3",
                "main.py",
                FLOPS_IMAGE_REGISTRY_URL,
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,
                f"--supported_platforms={supported_platforms}",
            )
        )

    def _configure_sla_components(self) -> None:
        assert self.parent_app
        parent_app_id = self.parent_app.app_id
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=f"builder{get_shortened_unique_id(parent_app_id)}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/oakestra/addon-flops/image-builder:latest",
                    one_shot_service=True,
                    cmd=self._prepare_cmd(),
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(
                    # TODO fine-tune -> Currently the Trained-Model Image Builder
                    # has a flaky deployment behavior "NoActiveClustersWithCapacity" is shown
                    # but when undeploy and redeploy manually it works.
                    memory=0,  # 2000,
                    vcpus=0,  # 1,
                    storage=0,  # 15000,
                ),
                privileged=True,
                constraints=[AddonConstraint(needs=[IMAGE_BUILDER_ADDON_TYPE])],
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
