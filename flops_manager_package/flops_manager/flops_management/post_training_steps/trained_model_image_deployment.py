from __future__ import annotations

from typing import TYPE_CHECKING

from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.image_management.trained_model_images import get_trained_model_image_name
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger

if TYPE_CHECKING:
    from flops_manager.classes.apps.project import FLOpsProject


def handle_trained_model_image_deployment(flops_project: FLOpsProject, run_id: str) -> None:
    msg = "Start handling FL post training step: Deployment of trained model image."
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    helper_app = FLOpsHelperApp.get_app(customer_id=flops_project.customer_id)
    trained_model_name = get_trained_model_image_name(
        customer_id=flops_project.customer_id, run_id=run_id
    )

    logger.debug("REEEEEEEEEEEEEEEEEEElelele")
