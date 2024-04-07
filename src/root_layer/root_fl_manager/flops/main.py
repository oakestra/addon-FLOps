import threading

from flops.classes.builder import FLClientEnvImageBuilder
from flops.classes.ml_repo import MlRepo
from flops.classes.process import FlOpsProcess
from flops.classes.ui import FLUserInterface
from flops.image_registry.main import fetch_latest_matching_image
from flops.utils import notify_ui
from utils.logging import logger
from utils.types import FlOpsProcessSla


def handle_fl_operations(flops_process: FlOpsProcess, fl_client_image: str) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(flops_process_id=flops_process.flops_process_id, msg=msg)
    # handle_aggregator(flops_process)
    # TODO


def handle_new_flops_process(new_flops_process_sla: FlOpsProcessSla, bearer_token: str) -> None:
    flops_process = FlOpsProcess(
        customer_id=new_flops_process_sla["customerID"],
        verbose=new_flops_process_sla.get("verbose", False),
    )
    fl_ui = FLUserInterface(flops_process=flops_process)
    fl_ui.deploy(bearer_token)

    ml_repo = MlRepo(
        flops_process_id=flops_process.flops_process_id,
        url=new_flops_process_sla["code"],
    )
    latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if latest_matching_image_name is not None:
        info_msg = f"Latest FL Client ENV image already exists for provided repo: '{ml_repo.name}'"
        if flops_process.verbose:
            info_msg += f" - image name : '{latest_matching_image_name}'"
        logger.info(info_msg)
        notify_ui(flops_process_id=flops_process.flops_process_id, msg=info_msg)
        threading.Thread(
            target=handle_fl_operations,
            args=(
                flops_process,
                latest_matching_image_name,
            ),
        ).start()
        return

    if flops_process.verbose:
        notify_ui(
            flops_process_id=flops_process.flops_process_id,
            msg="New FL Client image needs to be build. Start build delegation processes.",
        )

    FLClientEnvImageBuilder(flops_process=flops_process, ml_repo=ml_repo, ui=fl_ui).deploy()

    if flops_process.verbose:
        notify_ui(
            flops_process_id=flops_process.flops_process_id,
            msg="New Builder application created & deployed",
        )
