import argparse

from args_parser.fl_actors import prepare_fl_actors_argparsers
from args_parser.trained_model import prepare_trained_model_argparsers
from context.fl_actors import ContextFLActors
from context.trained_model import ContextTrainedModel


def parse_arguments_and_execute() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "image_registry_url",
        type=str,
        help="The URL of the image registry the build image should be pushed to.",
    )
    parser.add_argument("flops_project_id", type=str)
    parser.add_argument(
        "mqtt_ip",
        type=str,
        help="The MQTT IP to be able to notify the FLOps manager about the image build.",
    )
    parser.add_argument("project_observer_ip", type=str)
    parser.add_argument(
        "--deactivate-notifications",
        action="store_true",
        default=False,
        help="Deactivates MQTT for local debugging",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    prepare_fl_actors_argparsers(subparsers)
    prepare_trained_model_argparsers(subparsers)

    args = parser.parse_args()
    common_attributes = {
        "flops_project_id": args.flops_project_id,
        "image_registry_url": args.image_registry_url,
        "mqtt_ip": args.mqtt_ip,
        "project_observer_ip": args.project_observer_ip,
        "deactivate_notifications": args.deactivate_notifications,
    }
    if args.command == "fl_actors":
        ContextFLActors(
            **{
                **common_attributes,
                "ml_model_flavor": args.ml_model_flavor,
                "repo_url": args.repo_url,
                "use_devel_base_images": args.use_devel_base_images,
            },
        )
        return

    if args.command == "trained_model":
        ContextTrainedModel(
            **{**common_attributes, "run_id": args.run_id},
        )
