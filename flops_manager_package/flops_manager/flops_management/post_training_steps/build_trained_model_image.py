from __future__ import annotations

from typing import TYPE_CHECKING

from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.observatory.tracking_server.management import (
    get_tracking_server,
)
from flops_manager.classes.services.project.builders.trained_model_builder import (
    TrainedModelImageBuilder,
)
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.types import PostTrainingSteps
from flops_utils.logging import colorful_logger as logger

if TYPE_CHECKING:
    from flops_manager.classes.apps.project import FLOpsProject


def init_fl_post_training_steps(flops_project: FLOpsProject, winner_model_run_id: str) -> None:
    if PostTrainingSteps.BUILD_IMAGE_FOR_TRAINED_MODEL not in flops_project.post_training_steps:
        msg = "No further post training steps requested."
        logger.info(msg)
        notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)
        return

    msg = "Start handling FL post training. Preparing to build image based on best trained model."
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)
    project_observer = retrieve_from_db_by_project_id(
        FLOpsProjectObserver, flops_project.flops_project_id
    )
    tracking_server = get_tracking_server(flops_project.customer_id)
    TrainedModelImageBuilder(
        tracking_server_uri=tracking_server.get_url(),
        run_id=winner_model_run_id,
        parent_app=flops_project,
        project_observer_ip=project_observer.ip,  # type: ignore
    )
