from flops_manager.classes.oak.deployables.project_services.aggregator.main import FLAggregator
from flops_manager.classes.oak.deployables.project_services.learners import FLLearners
from flops_manager.database.common import retrieve_from_db
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_aggregator_success(aggregator_success_msg: dict) -> None:
    logger.debug("Aggregator successfully finished training.")
    flops_project_id = aggregator_success_msg["flops_project_id"]
    retrieve_from_db(FLAggregator, flops_project_id).undeploy()
    retrieve_from_db(FLLearners, flops_project_id).undeploy()
    # TODO


def handle_aggregator_failed(aggregator_failed_msg: dict) -> None:
    logger.debug(aggregator_failed_msg)
    flops_project_id = aggregator_failed_msg["flops_project_id"]
    retrieve_from_db(FLAggregator, flops_project_id).undeploy()
    retrieve_from_db(FLLearners, flops_project_id).undeploy()

    msg = "Aggregator failed. Terminating this FLOps Project."
    logger.critical(msg)
    notify_ui(flops_project_id=flops_project_id, msg=msg)
