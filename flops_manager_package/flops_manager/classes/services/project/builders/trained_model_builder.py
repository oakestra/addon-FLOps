from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.project.builders.base_builder import FLOpsBaseImageBuilder
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.types import PostTrainingSteps
from flops_utils.logging import logger
from pydantic import Field


class TrainedModelImageBuilder(FLOpsBaseImageBuilder):
    tracking_server_uri: str = Field(examples=["http://192.168.178.44:7027"])
    run_id: str = Field(description="The MLflow run-id of the trained model")

    def _prepare_cmd(self) -> str:
        cmd = super()._prepare_cmd()
        cmd += (
            f" trained_model {self.parent_app.customer_id} {self.tracking_server_uri} {self.run_id}"
        )
        return cmd

    @classmethod
    def handle_builder_success(cls, builder_success_msg: dict) -> None:
        flops_project_id = super().handle_builder_success(builder_success_msg)
        flops_project = retrieve_from_db_by_project_id(FLOpsProject, flops_project_id)

        msg = (
            "Start handling FL post training. Preparing to build image based on best trained model."
        )
        logger.info(msg)
        notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

        if PostTrainingSteps.DEPLOY_TRAINED_MODEL_IMAGE not in flops_project.post_training_steps:
            msg = "No further post training steps requested."
            logger.info(msg)
            notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)
            return

        msg = "Start handling FL post training step: deployment of trained model image."
        logger.info(msg)
        notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)
        # TODO
