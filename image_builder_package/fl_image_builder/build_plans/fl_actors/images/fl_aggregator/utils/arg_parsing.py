import argparse

from flops_utils.types import AggregatorType
from utils.aggregator_context import AggregatorContext


def parse_args() -> AggregatorContext:
    parser = argparse.ArgumentParser()

    parser.add_argument("flops_project_id", type=str)
    parser.add_argument(
        "mqtt_ip",
        type=str,
        help="The MQTT IP to be able to notify the FLOps manager.",
    )
    parser.add_argument("project_observer_ip", type=str)
    parser.add_argument("mlflow_tracking_server_url", type=str)

    parser.add_argument("aggregator_type", type=str)

    parser.add_argument("training_iterations", type=int)
    parser.add_argument("min_available_clients", type=int)
    parser.add_argument("min_fit_clients", type=int)
    parser.add_argument("min_evaluate_clients", type=int)

    # Only used for cluster-aggregators.
    parser.add_argument("root_aggregator_ip", type=str, nargs="?", default="")

    parser.add_argument(
        "--track-locally",
        action="store_true",
        default=False,
        help="Does not use the remote Tracking Server",
    )

    parser.add_argument(
        "--deactivate-notifications",
        action="store_true",
        default=False,
        help="Deactivates MQTT for local debugging",
    )

    args = parser.parse_args()

    return AggregatorContext(
        flops_project_id=args.flops_project_id,
        mqtt_ip=args.mqtt_ip,
        project_observer_ip=args.project_observer_ip,
        mlflow_tracking_server_url=args.mlflow_tracking_server_url,
        aggregator_type=AggregatorType(args.aggregator_type),
        training_iterations=args.training_iterations,
        min_available_clients=args.min_available_clients,
        min_fit_clients=args.min_fit_clients,
        min_evaluate_clients=args.min_evaluate_clients,
        track_locally=args.track_locally,
        deactivate_notifications=args.deactivate_notifications,
        root_aggregator_ip=args.root_aggregator_ip,
    )
