import sys

from context.main import get_context
from flops_utils.logging import logger
from flops_utils.notifications import notify_flops_manager, notify_project_observer


def _notify_flops_manager(
    topic: str,
    error_msg: str = None,
    msg_payload: dict = {},
) -> None:
    build_context = get_context()
    logger.info(error_msg)
    if build_context.deactivate_notifications:
        return
    notify_flops_manager(
        flops_project_id=build_context.flops_project_id,
        mqtt_ip=build_context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
        msg_payload=msg_payload,
    )


def notify_observer(msg: str) -> None:
    build_context = get_context()
    logger.info(msg)
    if build_context.deactivate_notifications:
        return
    notify_project_observer(project_observer_ip=build_context.project_observer_ip, msg=msg)


def notify_about_successful_builder_process() -> None:
    msg_payload = {}
    for name, time_frame in get_context().timer.time_frames.items():
        msg_payload[name] = time_frame.get_duration(human_readable=True)

    _notify_flops_manager(topic="flops_manager/image_builder/success", msg_payload=msg_payload)
    notify_observer(msg=str(msg_payload))


def notify_about_failed_build_and_terminate(error_msg: str) -> None:
    _notify_flops_manager("flops_manager/image_builder/failed", error_msg)
    notify_observer(error_msg)
    sys.exit(1)
