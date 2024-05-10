import threading

from flops_manager.classes.apps.observatory import FLOpsObservatory
from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.project.builder.main import FLOpsImageBuilder
from flops_manager.fl_management import handle_fl_operations
from flops_manager.image_management import check_if_latest_matching_images_exist
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger


def handle_new_flops_project(request_data: dict, bearer_token: str) -> None:
    # TODO check if observatory already exists and fetch it instead of creating a new one
    observatory = FLOpsObservatory.model_validate(request_data)
    flops_project = FLOpsProject.model_validate(request_data)

    project_observer = FLOpsProjectObserver(
        parent_app=observatory,
        flops_project=flops_project,
        bearer_token=bearer_token,
    )

    if check_if_latest_matching_images_exist(
        ml_repo_url=flops_project.ml_repo_url,
        ml_repo_latest_commit_hash=flops_project.ml_repo_latest_commit_hash,
    ):
        info_msg = "Latest FLOps images already exists for the provided repo."
        logger.info(info_msg)
        notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=info_msg)
        threading.Thread(target=handle_fl_operations, args=(flops_project,)).start()
        return

    FLOpsImageBuilder(parent_app=flops_project, project_observer_ip=project_observer.ip)
