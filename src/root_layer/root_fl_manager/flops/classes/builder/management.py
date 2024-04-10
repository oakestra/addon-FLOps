import flops.main as main_flops
from flops.classes.builder.main import FLClientEnvImageBuilder
from flops.classes.ml_repo import MlRepo
from flops.classes.project import FlOpsProject
from flops.classes.ui import FLUserInterface
from flops.utils import notify_ui
from utils.logging import logger


def init_builder(flops_project: FlOpsProject, ml_repo: MlRepo, fl_ui: FLUserInterface) -> None:
    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="New FL Client image needs to be build. Start build delegation processes.",
        )

    FLClientEnvImageBuilder(flops_project=flops_project, ml_repo=ml_repo, ui=fl_ui)

    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="New Builder application created & deployed",
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
