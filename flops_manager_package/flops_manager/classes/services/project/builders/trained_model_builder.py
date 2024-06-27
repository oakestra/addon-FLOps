from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.project.builders.base_builder import FLOpsBaseImageBuilder
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.flops_management.post_training_steps.trained_model_image_deployment import (
    handle_trained_model_image_deployment,
)
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.types import PostTrainingSteps
from flops_utils.logging import logger
from pydantic import Field


class TrainedModelImageBuilder(FLOpsBaseImageBuilder):
    tracking_server_uri: str = Field(examples=["http://192.168.178.44:7027"])
    run_id: str = Field(description="The MLflow run-id of the trained model")

    def _prepare_cmd(self) -> str:
        cmd = super()._prepare_cmd()
        cmd += " " + " ".join(
            (
                "trained_model",
                self.parent_app.customer_id,  # type: ignore
                self.tracking_server_uri,
                self.run_id,
            )
        )
        return cmd

    @classmethod
    def handle_builder_success(cls, builder_success_msg: dict) -> None:
        logger.debug(builder_success_msg)
        flops_project_id = builder_success_msg["flops_project_id"]
        builder = retrieve_from_db_by_project_id(cls, flops_project_id)
        run_id = builder.run_id  # type: ignore
        builder.undeploy()  # type: ignore

        flops_project = retrieve_from_db_by_project_id(FLOpsProject, flops_project_id)

        msg = (
            "Start handling FL post training. Preparing to build image based on best trained model."
        )
        logger.info(msg)
        notify_project_observer(
            flops_project_id=flops_project.flops_project_id,  # type: ignore
            msg=msg,
        )
        post_training_steps = flops_project.post_training_steps  # type: ignore
        if PostTrainingSteps.DEPLOY_TRAINED_MODEL_IMAGE not in post_training_steps:
            msg = "No further post training steps requested."
            logger.info(msg)
            notify_project_observer(
                flops_project_id=flops_project.flops_project_id,  # type: ignore
                msg=msg,
            )
            return

        handle_trained_model_image_deployment(
            flops_project=flops_project,  # type: ignore
            run_id=run_id,
        )
