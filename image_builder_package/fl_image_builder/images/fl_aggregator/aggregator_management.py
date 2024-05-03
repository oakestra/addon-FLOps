import flwr as fl
import mlflow
from flops_utils.notifications import notify_flops_ui
from notification_management import (
    notify_about_failure_and_terminate,
    notify_about_successful_completion,
)
from prometheus_client import Gauge, start_http_server
from strategy import OakFedAvg
from utils.aggregator_context import AggregatorContext

# Define gauges to track the global model accuracy & loss
accuracy_gauge = Gauge("model_accuracy", "Current accuracy of the global model")
loss_gauge = Gauge("model_loss", "Current loss of the global model")

FL_START_INFO_TEXT = """
Start Aggregator activities - Start Federated Learning:
Visit the page below to observe your (active) FLOps Project.
(Note: There you can observe the progress in real time.)
"""


def start_fl_server(aggregator_context: AggregatorContext, strategy, rounds):
    notify_flops_ui(
        flops_ui_ip=aggregator_context.flops_ui_ip,
        msg=f"{FL_START_INFO_TEXT}\n '{aggregator_context.mlflow_tracking_server_url}'",
    )

    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=rounds),
        strategy=strategy,
    )

    notify_about_successful_completion(aggregator_context=aggregator_context)


def handle_aggregator(aggregator_context: AggregatorContext) -> None:
    try:
        mlflow.set_tracking_uri(aggregator_context.mlflow_tracking_server_url)

        # Note: A mlflow experimnent consists of multiple runs.
        # For FLOps: experiment = project, run = Flower FL training + evaluation round.
        mlflow_experiment = mlflow.set_experiment(
            experiment_name=f"FLOps Project {aggregator_context.flops_project_id}"
        )

        start_http_server(8000)

        strategy_instance = OakFedAvg(
            mlflow_experiment_id=mlflow_experiment.experiment_id,
            accuracy_gauge=accuracy_gauge,
            loss_gauge=loss_gauge,
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
        notify_about_failure_and_terminate(
            aggregator_context=aggregator_context,
            error_msg=f"Aggregator failed: '{e}'",
        )
