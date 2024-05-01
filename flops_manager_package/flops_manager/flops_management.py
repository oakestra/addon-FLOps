import threading

from flops_manager.classes.oak.deployables.project_services.builder.main import FLOpsImageBuilder
from flops_manager.classes.oak.deployables.ui import FLOpsUserInterface
from flops_manager.classes.oak.project import FlOpsProject
from flops_manager.fl_management import handle_fl_operations
from flops_manager.image_management import check_if_latest_matching_images_exist
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger
from icecream import ic


def handle_new_flops_project(request_data: dict, bearer_token: str) -> None:
    flops_project = FlOpsProject.model_validate(request_data)
    ui = FLOpsUserInterface(flops_project=flops_project, bearer_token=bearer_token)

    if check_if_latest_matching_images_exist(flops_project.ml_repo_info):
        info_msg = "Latest FLOps images already exists for the provided repo."
        logger.info(info_msg)
        notify_ui(flops_project_id=flops_project.flops_project_id, msg=info_msg)
        threading.Thread(target=handle_fl_operations, args=(flops_project,)).start()
        return

    # FLOpsImageBuilder(flops_project=flops_project, ui=ui)
