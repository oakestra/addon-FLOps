import threading

from flops.aggregator_management.main import handle_aggregator
from flops.fl_ui_management.main import FLUserInterface
from flops.fl_ui_management.notification import notify_ui
from flops.image_builder_management.common import MlRepo
from flops.image_builder_management.main import FLClientEnvImageBuilder
from flops.image_registry.main import fetch_latest_matching_image
from flops.process import FlOpsProcess
from icecream import ic
from utils.logging import logger
from utils.types import FlOpsProcessSla


def handle_fl_operations(flops_process: FlOpsProcess, fl_client_image: str) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_ui(msg, flops_process)
    # handle_aggregator(flops_process)
    # TODO


def handle_new_flops_process(new_flops_process_sla: FlOpsProcessSla, bearer_token: str) -> None:
    flops_process = FlOpsProcess(
        customer_id=new_flops_process_sla["customerID"],
        verbose=new_flops_process_sla.get("verbose", False),
    )
    FlOpsProcess()

    fl_ui = FLUserInterface(flops_process_id=flops_process.flops_process_id)
    fl_ui.deploy(flops_process, bearer_token)
    ml_repo = MlRepo(
        flops_process_id=flops_process.flops_process_id,
        url=new_flops_process_sla["code"],
    )
    ic("DDDDDDDDDDDD", ml_repo)
    return
    latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if latest_matching_image_name is not None:
        info_msg = f"Latest FL Client ENV image already exists for provided repo: '{ml_repo.name}'"
        if flops_process.verbose:
            info_msg += f" - image name : '{latest_matching_image_name}'"
        logger.info(info_msg)
        notify_ui(info_msg, flops_process.flops_process_id)

        threading.Thread(
            target=handle_fl_operations,
            args=(
                flops_process,
                latest_matching_image_name,
            ),
        ).start()
        return

    ic("EEEEEEEEEEEEE")
    FLClientEnvImageBuilder(flops_process, ml_repo, fl_ui)
