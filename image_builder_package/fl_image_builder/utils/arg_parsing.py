import argparse

from utils.build_context import BuildContext


def parse_args() -> None:
    parser = argparse.ArgumentParser(description="Process GitHub repository and service ID.")

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
    parser.add_argument("flops_ui_ip", type=str)

    parser.add_argument(
        "--develop",
        action="store_true",
        default=False,
        help="Use builder in develop/debug mode, e.g. deactivates MQTT.",
    )

    args = parser.parse_args()

    BuildContext(
        repo_url=args.repo_url,
        image_registry_url=args.image_registry_url,
        flops_project_id=args.flops_project_id,
        mqtt_ip=args.mqtt_ip,
        flops_ui_ip=args.flops_ui_ip,
        develop=args.develop,
    )
