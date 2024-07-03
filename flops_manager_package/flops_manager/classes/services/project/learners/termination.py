from flops_manager.classes.services.project.aggregators.auxiliary import (
    get_matching_aggregator_class_based_on_project_id,
)
from flops_utils.logging import colorful_logger as logger


def handle_learner_failed(learner_failed_msg: dict) -> None:
    """FUTURE WORK: For now simply terminate the FLops Project

    This includes terminating all connected aggregators.
    """
    logger.debug(learner_failed_msg)
    flops_project_id = learner_failed_msg["flops_project_id"]
    # NOTE: The learners will be undeployed as part of the aggregation failure handling.
    # TODO: Decouple this.

    # TODO: By improving this code a couple of redundant DB calls can be omitted.
    aggregator_class = get_matching_aggregator_class_based_on_project_id(flops_project_id)
    aggregator_class.handle_aggregator_failed(learner_failed_msg)  # type: ignore
