import flops_manager.flops.main as main_flops
from flops_manager.flops.classes.builder.main import FLClientEnvImageBuilder
from flops_manager.flops.classes.ml_repo import MlRepo
from flops_manager.flops.classes.project import FlOpsProject
from flops_manager.flops.classes.ui import UserInterface
from flops_manager.flops.utils import notify_ui
from flops_manager.utils.logging import logger


def init_builder(flops_project: FlOpsProject, ml_repo: MlRepo, ui: UserInterface) -> None:
    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="New FL Client image needs to be build. Start build delegation processes.",
        )

    FLClientEnvImageBuilder(flops_project=flops_project, ml_repo=ml_repo, ui=ui)

    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="New Builder service created & deployed",
        )


def handle_builder_success(builder_success_msg: dict) -> None:
    logger.debug(builder_success_msg)
    flops_project_id = builder_success_msg["flops_project_id"]
    FLClientEnvImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
    main_flops.handle_fl_operations(
        flops_project=FlOpsProject.retrieve_from_db(flops_project_id=flops_project_id),
        fl_client_image=builder_success_msg["image_name_with_tag"],
    )


def handle_builder_failed(builder_failed_msg: dict) -> None:
    logger.debug(builder_failed_msg)
    flops_project_id = builder_failed_msg["flops_project_id"]
    FLClientEnvImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
    msg = "Builder failed. Terminating this FLOps."
    logger.critical(msg)
    notify_ui(flops_project_id=flops_project_id, msg=msg)
