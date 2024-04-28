import threading

from flops_manager.classes.ml_repo import MlRepo
from flops_manager.classes.oak.deployables.project_services.builder.main import FLOpsImageBuilder
from flops_manager.classes.oak.deployables.ui import FLOpsUserInterface
from flops_manager.classes.oak.project import FlOpsProject
from flops_manager.image_registry_management.main import check_if_latest_matching_images_exists
from flops_manager.manage_fl import handle_fl_operations
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_new_flops_project(request_data: dict, bearer_token: str) -> None:
    flops_project = FlOpsProject.model_validate(request_data)
    ui = FLOpsUserInterface(flops_project=flops_project, bearer_token=bearer_token)
    ml_repo = MlRepo(
        flops_project_id=flops_project.flops_project_id,
        url=flops_project.ml_repo_url,
    )
    latest_matching_images = check_if_latest_matching_images_exists(ml_repo)
    if latest_matching_images is not None:
        info_msg = f"Latest FL Learner image already exists for provided repo: '{ml_repo.name}'"
        if flops_project.verbose:
            info_msg += f" - image name : '{latest_matching_images}'"
        logger.info(info_msg)
        notify_ui(flops_project_id=flops_project.flops_project_id, msg=info_msg)
        threading.Thread(
            target=handle_fl_operations,
            args=(
                flops_project,
                latest_matching_images,
            ),
        ).start()
        return

    FLOpsImageBuilder(flops_project=flops_project, ml_repo=ml_repo, ui=ui)
