import sys

from flops_utils.mqtt_topics import SupportedTopic
from flops_utils.notifications import notify_flops_manager, notify_project_observer
from utils.aggregator_context import AggregatorContext


def _notify_flops_manager(
    aggregator_context: AggregatorContext,
    topic: SupportedTopic,
    error_msg: str = "",
) -> None:
    winner_model = aggregator_context.winner_model
    notify_flops_manager(
        flops_project_id=aggregator_context.flops_project_id,
        mqtt_ip=aggregator_context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
        msg_payload={
            "experiment_id": winner_model.experiment_id,
            "run_id": winner_model.run_id,
            "accuracy": winner_model.accuracy,
            "loss": winner_model.loss,
        },
    )


def notify_about_successful_completion(aggregator_context: AggregatorContext) -> None:
    _notify_flops_manager(
        aggregator_context=aggregator_context,
        topic=SupportedTopic.AGGREGATOR_SUCCESS,
    )
    winner_model = aggregator_context.winner_model
    notify_project_observer(
        project_observer_ip=aggregator_context.project_observer_ip,
        msg="\n".join(
            (
                "Aggregator tasks completed successfully.",
                "The best performing model:",
                f"- accuracy: {winner_model.accuracy}",
                f"- loss: {winner_model.loss}",
                f"- experiment_id: {winner_model.experiment_id}",
                f"- run_id: {winner_model.run_id}",
            )
        ),
    )


def notify_about_failure_and_terminate(
    aggregator_context: AggregatorContext,
    error_msg: str,
) -> None:
    _notify_flops_manager(
        aggregator_context=aggregator_context,
        topic=SupportedTopic.AGGREGATOR_FAILED,
        error_msg=error_msg,
    )
    notify_project_observer(
        project_observer_ip=aggregator_context.project_observer_ip,
        msg=error_msg,
    )
    sys.exit(1)
