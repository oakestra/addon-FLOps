from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.logging import logger


def handle_fl_operations(flops_project: FlOpsProject, fl_client_image: str) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(flops_project_id=flops_project.flops_project_id, msg=msg)
    # init_aggregator(flops_project=flops_project)
    # TODO
