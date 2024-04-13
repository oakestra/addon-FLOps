from flops_manager.classes.oakestratables.deployables.project_services.aggregator import (
    FLAggregator,
)
from flops_manager.classes.oakestratables.deployables.project_services.learner import FLLearner
from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.logging import logger


def handle_fl_operations(flops_project: FlOpsProject, fl_learner_image: str) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(flops_project_id=flops_project.flops_project_id, msg=msg)

    FLAggregator(flops_project=flops_project)
    FLLearner(flops_project=flops_project, fl_learner_image=fl_learner_image)

    # TODO
