import argparse

from flops_utils.types import MLModelFlavor
from utils.builder_context import BuilderContext

DEVEL_HELP_TXT = """
Reuses special base images that already include the ML repo dependencies.
Intended for the development of the image builder.
Helps skip/reuse lengthy dependency resolutions, etc.
Only works if the provided repo_url has a matching dependency base image in Github.
"""


def parse_args() -> BuilderContext:
    parser = argparse.ArgumentParser(description="Process GitHub repository and service ID.")

    parser.add_argument("ml_model_flavor", type=MLModelFlavor)
    parser.add_argument("repo_url", type=str, help="The URL of the GitHub repository.")
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
        "--use_devel_base_images",
        action="store_true",
        default=False,
        help=DEVEL_HELP_TXT,
    )

    parser.add_argument(
        "--deactivate_notifications",
        action="store_true",
        default=False,
        help="Deactivates MQTT for local debugging",
    )

    args = parser.parse_args()

    return BuilderContext(
        ml_model_flavor=args.ml_model_flavor,
        repo_url=args.repo_url,
        image_registry_url=args.image_registry_url,
        flops_project_id=args.flops_project_id,
        mqtt_ip=args.mqtt_ip,
        project_observer_ip=args.project_observer_ip,
        deactivate_notifications=args.deactivate_notifications,
        use_devel_base_images=args.use_devel_base_images,
    )
