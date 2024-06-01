from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.observatory.tracking_server.management import (
    get_tracking_server,
)
from flops_manager.classes.services.project.aggregator.main import FLAggregator
from flops_manager.classes.services.project.learners import FLLearners
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.types import PostTrainingSteps
from flops_utils.logging import colorful_logger as logger


def handle_fl_training_processes(flops_project: FLOpsProject) -> None:
    msg = "Start handling FL training processes"
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    tracking_server = get_tracking_server(flops_project.customer_id)
    project_observer = retrieve_from_db_by_project_id(
        FLOpsProjectObserver, flops_project.flops_project_id
    )

    fl_aggregator = FLAggregator(
        parent_app=flops_project,
        project_observer_ip=project_observer.ip,
        tracking_server_url=tracking_server.get_url(),
    )
    FLLearners(parent_app=flops_project, fl_aggregator_ip=fl_aggregator.ip)


def init_fl_post_training_steps(flops_project: FLOpsProject) -> None:
    if PostTrainingSteps.BUILD_IMAGE_FOR_TRAINED_MODEL not in flops_project.post_training_steps:
        msg = "No further post training steps requested."
        logger.info(msg)
        notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)
        return

    msg = "Start handling FL post training. Preparing to build image based on best trained model."
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    # TODO
