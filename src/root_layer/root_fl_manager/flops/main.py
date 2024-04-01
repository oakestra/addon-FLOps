from fl_ui_management.main import create_fl_ui_service, deploy_fl_ui_service
from fl_ui_management.notification import notify_ui
from flops.identifier import FlOpsIdentifier
from image_builder_management.common import MlRepo
from image_builder_management.main import delegate_image_build
from image_registry.main import fetch_latest_matching_image
from utils.logging import logger
from utils.types import FlSla


def handle_new_fl_service(
    new_fl_service_sla: FlSla,
    auth_header: str,
    verbose: bool = False,
) -> None:
    flops_identifier = FlOpsIdentifier()

    fl_ui_service_id = create_fl_ui_service(new_fl_service_sla, auth_header, flops_identifier)
    deploy_fl_ui_service(fl_ui_service_id)

    ml_repo = MlRepo(new_fl_service_sla["code"])
    latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if latest_matching_image_name is not None:
        info_msg = f"Latest FL Client ENV image already exists for provided repo: '{ml_repo.name}'"
        notify_ui(info_msg, flops_identifier)
        logger.info(info_msg)
        return

    delegate_image_build(flops_identifier, ml_repo, verbose)
