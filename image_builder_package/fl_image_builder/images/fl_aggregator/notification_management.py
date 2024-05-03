import sys

from flops_utils.notifications import notify_flops_manager, notify_flops_ui
from utils.aggregator_context import AggregatorContext


def _notify_flops_manager(
    aggregator_context: AggregatorContext,
    topic: str,
    error_msg: str = None,
) -> None:
    notify_flops_manager(
        flops_project_id=aggregator_context.flops_project_id,
        mqtt_ip=aggregator_context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
    )


def notify_about_successful_completion(aggregator_context: AggregatorContext) -> None:
    _notify_flops_manager(
        aggregator_context=aggregator_context,
        topic="flops_manager/aggregator/success",
    )
    notify_flops_ui(
        flops_ui_ip=aggregator_context.flops_ui_ip,
        msg="Aggregator tasks completed successfully.",
    )


def notify_about_failure_and_terminate(
    aggregator_context: AggregatorContext,
    error_msg: str,
) -> None:
    _notify_flops_manager(
        aggregator_context=aggregator_context,
        topic="flops_manager/aggregator/failed",
        error_msg=error_msg,
    )
    notify_flops_ui(
        flops_ui_ip=aggregator_context.flops_ui_ip,
        msg=error_msg,
    )
    sys.exit(1)
