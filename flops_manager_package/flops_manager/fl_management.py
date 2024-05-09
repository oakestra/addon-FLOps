from flops_manager.classes.deployables.project_services.aggregator.main import FLAggregator
from flops_manager.classes.deployables.project_services.learners import FLLearners
from flops_manager.classes.deployables.ui import FLOpsUserInterface
from flops_manager.classes.project import FLOpsProject
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_fl_operations(flops_project: FLOpsProject) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(flops_project_id=flops_project.flops_project_id, msg=msg)

    ui = retrieve_from_db_by_project_id(FLOpsUserInterface, flops_project.flops_project_id)

    fl_aggregator = FLAggregator(flops_project=flops_project, flops_ui_ip=ui.ip)
    FLLearners(flops_project=flops_project, fl_aggregator=fl_aggregator)

    # TODO
