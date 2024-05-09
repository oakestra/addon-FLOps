import sys

from flops_utils.logging import logger
from flops_utils.notifications import notify_flops_manager, notify_project_observer
from utils.build_context import get_build_context


def _notify_flops_manager(topic: str, error_msg: str = None) -> None:
    build_context = get_build_context()
    if build_context.develop:
        logger.fatal(f"DEVEL: {error_msg}")
        return
    notify_flops_manager(
        flops_project_id=build_context.flops_project_id,
        mqtt_ip=build_context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
    )


def notify_ui(msg: str) -> None:
    build_context = get_build_context()
    if build_context.develop:
        logger.info(f"DEVEL: {msg}")
        return
    notify_project_observer(
        project_observer_ip=build_context.project_observer_ip, msg=msg
    )


def notify_about_successful_build() -> None:
    _notify_flops_manager(topic="flops_manager/image_builder/success")


def notify_about_failed_build_and_terminate(error_msg: str) -> None:
    _notify_flops_manager("flops_manager/image_builder/failed", error_msg)
    notify_ui(error_msg)
    sys.exit(1)
