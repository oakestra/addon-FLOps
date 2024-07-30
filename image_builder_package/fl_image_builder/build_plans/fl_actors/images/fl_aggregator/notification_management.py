import sys

from flops_utils.mqtt_topics import SupportedTopic
from flops_utils.notifications import notify_flops_manager, notify_project_observer
from utils.aggregator_context import AggregatorContext


def builder_notify_flops_manager(
    aggregator_context: AggregatorContext,
    topic: SupportedTopic,
    error_msg: str = "",
) -> None:
    winner_model = aggregator_context.winner_model
    msg_payload = {
        "aggregator_type": aggregator_context.aggregator_type.value,
        **({"accuracy": winner_model.accuracy} if winner_model and winner_model.accuracy else {}),
        **({"loss": winner_model.loss} if winner_model and winner_model.loss else {}),
        **(
            {"experiment_id": winner_model.experiment_id}
            if aggregator_context.should_use_mlflow
            else {}
        ),
        **({"run_id": winner_model.run_id} if aggregator_context.should_use_mlflow else {}),
    }

    notify_flops_manager(
        flops_project_id=aggregator_context.flops_project_id,
        mqtt_ip=aggregator_context.mqtt_ip,
        topic=topic,
        error_msg=error_msg,
        msg_payload=msg_payload,
    )


def notify_about_successful_completion(aggregator_context: AggregatorContext) -> None:
    builder_notify_flops_manager(
        aggregator_context=aggregator_context,
        topic=SupportedTopic.AGGREGATOR_SUCCESS,
    )
    winner_model = aggregator_context.winner_model

    msg = "\n".join(
        (
            "Aggregator tasks completed successfully.",
            "The best performing model:",
            f"- accuracy: {winner_model.accuracy}",
            f"- loss: {winner_model.loss}",
        )
    )
    if aggregator_context.should_use_mlflow:
        msg += "\n" + "\n".join(
            (
                f"- experiment_id: {winner_model.experiment_id}",
                f"- run_id: {winner_model.run_id}",
            )
        )

    notify_project_observer(
        project_observer_ip=aggregator_context.project_observer_ip,
        msg=msg + f"({aggregator_context.aggregator_type.value})",
    )


def notify_about_failure_and_terminate(
    aggregator_context: AggregatorContext,
    error_msg: str,
) -> None:
    builder_notify_flops_manager(
        aggregator_context=aggregator_context,
        topic=SupportedTopic.AGGREGATOR_FAILED,
        error_msg=error_msg,
    )
    notify_project_observer(
        project_observer_ip=aggregator_context.project_observer_ip,
        msg=error_msg,
    )
    sys.exit(1)
