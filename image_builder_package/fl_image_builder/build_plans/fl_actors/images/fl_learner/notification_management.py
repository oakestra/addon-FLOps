import sys

from context import LearnerContext
from flops_utils.mqtt_topics import SupportedTopic
from flops_utils.notifications import notify_flops_manager, notify_project_observer

# NOTE: This code can be further refactored and made reusable.
# See Aggregator for more.


def _notify_flops_manager(
    context: LearnerContext,
    topic: SupportedTopic,
    error_msg: str = None,
) -> None:
    notify_flops_manager(
        flops_project_id=context.flops_project_id,
        mqtt_ip=context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
    )


def notify_about_failure_and_terminate(
    context: LearnerContext,
    error_msg: str,
) -> None:
    _notify_flops_manager(
        aggregator_context=context,
        topic=SupportedTopic.LEARNER_FAILED,
        error_msg=error_msg,
    )
    notify_project_observer(
        project_observer_ip=context.project_observer_ip,
        msg=error_msg,
    )
    sys.exit(1)
