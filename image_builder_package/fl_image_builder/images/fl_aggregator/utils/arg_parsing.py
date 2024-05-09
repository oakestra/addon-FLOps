import argparse

from utils.aggregator_context import AggregatorContext


def parse_args() -> AggregatorContext:
    parser = argparse.ArgumentParser()

    parser.add_argument("flops_project_id", type=str)
    parser.add_argument(
        "mqtt_ip",
        type=str,
        help="The MQTT IP to be able to notify the FLOps manager about the image build.",
    )
    parser.add_argument("project_observer_ip", type=str)
    parser.add_argument("mlflow_tracking_server_url", type=str)

    parser.add_argument("training_rounds", type=int)
    parser.add_argument("min_available_clients", type=int)
    parser.add_argument("min_fit_clients", type=int)
    parser.add_argument("min_evaluate_clients", type=int)

    args = parser.parse_args()

    return AggregatorContext(
        flops_project_id=args.flops_project_id,
        mqtt_ip=args.mqtt_ip,
        project_observer_ip=args.project_observer_ip,
        mlflow_tracking_server_url=args.mlflow_tracking_server_url,
        training_rounds=args.training_rounds,
        min_available_clients=args.min_available_clients,
        min_fit_clients=args.min_fit_clients,
        min_evaluate_clients=args.min_evaluate_clients,
    )
