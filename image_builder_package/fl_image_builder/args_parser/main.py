import argparse

from args_parser.fl_actors import prepare_fl_actors_argparsers
from args_parser.trained_model import prepare_trained_model_argparsers
from context.fl_actors import ContextFLActors
from context.main import Context
from context.trained_model import ContextTrainedModel
from flops_utils.types import PlatformSupport


def parse_arguments_and_set_context() -> Context:
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
        "--supported_platforms",
        default=PlatformSupport.LINUX_AMD64.value,
        help="A comma-separated list of supported/requested target platforms",
    )
    parser.add_argument(
        "--deactivate-notifications",
        action="store_true",
        default=False,
        help="Deactivates MQTT for local debugging",
    )

    subparsers = parser.add_subparsers(
        dest="build_plan",
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
        "supported_platforms": [
            PlatformSupport(platform) for platform in args.supported_platforms.split(",")
        ],
    }
    if args.build_plan == "fl_actors":
        return ContextFLActors(
            **{
                **common_attributes,
                "ml_model_flavor": args.ml_model_flavor,
                "repo_url": args.repo_url,
                "use_devel_base_images": args.use_devel_base_images,
            },
        )

    return ContextTrainedModel(
        **{
            **common_attributes,
            "customer_id": args.customer_id,
            "tracking_server_uri": args.tracking_server_uri,
            "run_id": args.run_id,
        },
    )
