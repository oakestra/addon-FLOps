from flops_manager.classes.deployables.project_services.builder.main import FLOpsImageBuilder
from flops_manager.classes.project import FLOpsProject
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.fl_management import handle_fl_operations
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_builder_success(builder_success_msg: dict) -> None:
    logger.debug(builder_success_msg)
    flops_project_id = builder_success_msg["flops_project_id"]
    retrieve_from_db_by_project_id(FLOpsImageBuilder, flops_project_id).undeploy()
    handle_fl_operations(
        flops_project=retrieve_from_db_by_project_id(FLOpsProject, flops_project_id)
    )


def handle_builder_failed(builder_failed_msg: dict) -> None:
    logger.debug(builder_failed_msg)
    flops_project_id = builder_failed_msg["flops_project_id"]
    retrieve_from_db_by_project_id(FLOpsImageBuilder, flops_project_id).undeploy()
    msg = "Builder failed. Terminating this FLOps Project."
    logger.critical(msg)
    notify_ui(flops_project_id=flops_project_id, msg=msg)
