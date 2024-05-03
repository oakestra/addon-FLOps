import argparse

from flops_ui.ui_context import UIContext


def parse_args() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("flops_id", type=str)
    parser.add_argument(
        "mqtt_ip",
        type=str,
        help="The MQTT Broker IP to be able to communicate with the the FL manager.",
    )
    parser.add_argument("mqtt_port", type=str)

    args = parser.parse_args()

    UIContext(
        args.flops_id,
        args.mqtt_ip,
        args.mqtt_port,
    )
