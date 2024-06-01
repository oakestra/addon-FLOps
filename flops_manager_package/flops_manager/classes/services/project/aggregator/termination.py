from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.project.aggregator.main import FLAggregator
from flops_manager.classes.services.project.learners import FLLearners
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.flops_management.post_training_steps.build_trained_model_image import (
    init_fl_post_training_steps,
)
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger


def handle_aggregator_success(aggregator_success_msg: dict) -> None:
    logger.debug("Aggregator successfully finished training.")
    flops_project_id = aggregator_success_msg["flops_project_id"]
    retrieve_from_db_by_project_id(FLAggregator, flops_project_id).undeploy()
    retrieve_from_db_by_project_id(FLLearners, flops_project_id).undeploy()
    init_fl_post_training_steps(
        flops_project=retrieve_from_db_by_project_id(FLOpsProject, flops_project_id),
        winner_model_run_id=aggregator_success_msg["run_id"],
    )


def handle_aggregator_failed(aggregator_failed_msg: dict) -> None:
    logger.debug(aggregator_failed_msg)
    flops_project_id = aggregator_failed_msg["flops_project_id"]
    retrieve_from_db_by_project_id(FLAggregator, flops_project_id).undeploy()
    retrieve_from_db_by_project_id(FLLearners, flops_project_id).undeploy()

    msg = "Aggregator failed. Terminating this FLOps Project."
    logger.critical(msg)
    notify_project_observer(flops_project_id=flops_project_id, msg=msg)
