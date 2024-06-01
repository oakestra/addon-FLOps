import argparse

from args_parser.common import Subparsers


def prepare_trained_model_argparsers(subparsers: Subparsers) -> None:
    trained_model_parser = subparsers.add_parser(
        "trained_model",
        help="command for image builds for trained models",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    trained_model_parser.add_argument("customer_id", type=str)
    trained_model_parser.add_argument("tracking_server_uri", type=str)
    trained_model_parser.add_argument(
        "run_id",
        type=str,
        help="The corresponding MLflow run ID of the trained model",
    )
