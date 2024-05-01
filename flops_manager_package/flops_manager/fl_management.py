from flops_manager.classes.oak.deployables.project_services.aggregator.main import FLAggregator
from flops_manager.classes.oak.deployables.project_services.learners import FLLearners
from flops_manager.classes.oak.deployables.ui import FLOpsUserInterface
from flops_manager.classes.oak.project import FlOpsProject
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_fl_operations(flops_project: FlOpsProject) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(flops_project_id=flops_project.flops_project_id, msg=msg)

    ui = FLOpsUserInterface.retrieve_from_db(flops_project.flops_project_id)

    fl_aggregator = FLAggregator(flops_project=flops_project, flops_ui_ip=ui.ip)
    FLLearners(flops_project=flops_project, fl_aggregator=fl_aggregator)

    # TODO
