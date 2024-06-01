from __future__ import annotations

from typing import TYPE_CHECKING

from flops_utils.logging import logger
from flops_utils.notifications import notify_flops_manager, notify_project_observer

if TYPE_CHECKING:
    from context.main import Context


def notify_manager(
    context: Context,
    topic: str,
    error_msg: str = None,
    msg_payload: dict = {},
) -> None:
    logger.info(error_msg)
    if context.deactivate_notifications:
        return
    notify_flops_manager(
        flops_project_id=context.flops_project_id,
        mqtt_ip=context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
        msg_payload=msg_payload,
    )


def notify_observer(context: Context, msg: str) -> None:
    logger.info(msg)
    if context.deactivate_notifications:
        return
    notify_project_observer(project_observer_ip=context.project_observer_ip, msg=msg)
