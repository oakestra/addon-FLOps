from http import HTTPStatus

import api.utils
from fl_ui_management.main import create_fl_ui_service
from fl_ui_management.notification import notify_ui
from image_builder_management.common import MlRepo
from image_builder_management.main import delegate_image_build
from image_registry.main import fetch_latest_matching_image
from utils.exceptions import FLUIServiceDeploymentException
from utils.identifier import FlOpsIdentifier
from utils.logging import logger
from utils.types import FL_SLA


def handle_new_fl_service(
    new_fl_service_sla: FL_SLA,
    auth_header: str,
    verbose: bool = False,
) -> None:
    flops_identifier = FlOpsIdentifier()
    fl_ui_service_id = create_fl_ui_service(new_fl_service_sla, auth_header, flops_identifier)

    status, _ = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint=f"/api/service/{fl_ui_service_id}/instance",
        what_should_happen=f"Deploy FL UI service '{fl_ui_service_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceDeploymentException()

    ml_repo = MlRepo(new_fl_service_sla["code"])
    status, latest_matching_image_name = fetch_latest_matching_image(ml_repo)
    if status != HTTPStatus.OK:
        err_msg = f"Failed to check latest image based on this repo name: '{ml_repo.name}'"
        notify_ui(err_msg, flops_identifier)
        logger.critical(err_msg)
        return

    if latest_matching_image_name is not None:
        info_msg = f"Latest FL Client ENV image already exists for provided repo: '{ml_repo.name}'"
        notify_ui(info_msg, flops_identifier)
        logger.info(info_msg)
        return

    delegate_image_build(flops_identifier, ml_repo, verbose)
