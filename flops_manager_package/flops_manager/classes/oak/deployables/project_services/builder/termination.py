from flops_manager.classes.oak.deployables.project_services.builder.main import FLOpsImageBuilder
from flops_manager.classes.oak.project import FlOpsProject
from flops_manager.fl_management import handle_fl_operations
from flops_manager.mqtt.sender import notify_ui
from flops_utils.logging import colorful_logger as logger


def handle_builder_success(builder_success_msg: dict) -> None:
    logger.debug(builder_success_msg)
    flops_project_id = builder_success_msg["flops_project_id"]
    FLOpsImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
    handle_fl_operations(
        flops_project=FlOpsProject.retrieve_from_db(flops_project_id=flops_project_id),
        fl_learner_image=builder_success_msg["learner_image_name_with_tag"],
        fl_aggregator_image=builder_success_msg["aggregator_image_name_with_tag"],
    )


def handle_builder_failed(builder_failed_msg: dict) -> None:
    logger.debug(builder_failed_msg)
    flops_project_id = builder_failed_msg["flops_project_id"]
    FLOpsImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
    msg = "Builder failed. Terminating this FLOps Project."
    logger.critical(msg)
    notify_ui(flops_project_id=flops_project_id, msg=msg)
