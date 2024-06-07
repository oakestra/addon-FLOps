import sys

import flwr as fl
import mlflow
from flops_utils.logging import logger
from flops_utils.notifications import notify_project_observer
from notification_management import (
    notify_about_failure_and_terminate,
    notify_about_successful_completion,
)
from strategy.main import FLOpsFedAvg
from utils.aggregator_context import AggregatorContext

FL_START_INFO_TEXT = """
Start Aggregator activities - Start Federated Learning:
Visit the page below to observe your (active) FLOps Project.
(Note: There you can observe the progress in real time.)
"""


def start_fl_server(aggregator_context: AggregatorContext, strategy, rounds):
    if not aggregator_context.deactivate_notifications:
        notify_project_observer(
            project_observer_ip=aggregator_context.project_observer_ip,
            msg=f"{FL_START_INFO_TEXT}\n '{aggregator_context.mlflow_tracking_server_url}'",
        )
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=rounds),
        strategy=strategy,
    )
    if not aggregator_context.deactivate_notifications:
        notify_about_successful_completion(aggregator_context=aggregator_context)


def handle_aggregator(aggregator_context: AggregatorContext) -> None:
    try:
        if not aggregator_context.track_locally:
            mlflow.set_tracking_uri(aggregator_context.mlflow_tracking_server_url)
        # NOTE: A MLflow experiment consists of multiple runs.
        # For FLOps: experiment = project, run = Flower FL training + evaluation round.
        mlflow_experiment = mlflow.set_experiment(
            experiment_name=f"FLOps Project {aggregator_context.flops_project_id}"
        )
        strategy_instance = FLOpsFedAvg(
            aggregator_context=aggregator_context,
            mlflow_experiment_id=mlflow_experiment.experiment_id,
            # NOTE: The Flower Strategy lacks the notion of the number of expected training rounds.
            requested_total_number_of_training_rounds=aggregator_context.training_rounds,
            min_available_clients=aggregator_context.min_available_clients,
            min_fit_clients=aggregator_context.min_fit_clients,
            min_evaluate_clients=aggregator_context.min_evaluate_clients,
        )
        start_fl_server(
            aggregator_context=aggregator_context,
            strategy=strategy_instance,
            rounds=aggregator_context.training_rounds,
        )

    except Exception as e:
        if aggregator_context.deactivate_notifications:
            logger.exception("Aggregation failed with exception.")
            sys.exit(1)

        notify_about_failure_and_terminate(
            aggregator_context=aggregator_context,
            error_msg=f"Aggregator failed: '{e}'",
        )
