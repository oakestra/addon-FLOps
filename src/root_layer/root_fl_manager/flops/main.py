import threading

from flops.classes.builder import FLClientEnvImageBuilder
from flops.classes.ml_repo import MlRepo
from flops.classes.project import FlOpsProject
from flops.classes.ui import FLUserInterface
from flops.image_registry.main import fetch_latest_matching_image
from flops.utils import notify_ui
from utils.logging import logger
from utils.types import FlOpsProjectSla


def handle_fl_operations(flops_project: FlOpsProject, fl_client_image: str) -> None:
    msg = "Start handling FL project"
    logger.info(msg)
    notify_ui(flops_project_id=flops_project.flops_project_id, msg=msg)

    # FLClientEnvImageBuilder(flops_project=flops_project, ml_repo=ml_repo, ui=fl_ui)
    # if flops_project.verbose:
    #     notify_ui(
    #         flops_project_id=flops_project.flops_project_id,
    #         msg="New FL Aggregator service created & deployed",
    #     )
    # handle_aggregator(flops_project)
    # TODO


def handle_new_flops_project(new_flops_project_sla: FlOpsProjectSla, bearer_token: str) -> None:
    from icecream import ic

    ic("Zaaaaaaaaa")
    flops_project = FlOpsProject(
        customer_id=new_flops_project_sla["customerID"],
        verbose=new_flops_project_sla.get("verbose", False),
    )
    ic("Zbbbbbbbbb")
    fl_ui = FLUserInterface(flops_project=flops_project, bearer_token=bearer_token)
    ic("ZzzzzzzzzzzzzzzzzzzzZ")
    return
    ml_repo = MlRepo(
        flops_project_id=flops_project.flops_project_id,
        url=new_flops_project_sla["code"],
    )
    latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if latest_matching_image_name is not None:
        info_msg = f"Latest FL Client ENV image already exists for provided repo: '{ml_repo.name}'"
        if flops_project.verbose:
            info_msg += f" - image name : '{latest_matching_image_name}'"
        logger.info(info_msg)
        notify_ui(flops_project_id=flops_project.flops_project_id, msg=info_msg)
        threading.Thread(
            target=handle_fl_operations,
            args=(
                flops_project,
                latest_matching_image_name,
            ),
        ).start()
        return

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
