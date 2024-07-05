import argparse
from typing import List, Tuple

from context import LearnerContext


def parse_args() -> Tuple[str, List[str]]:  # type: ignore
    parser = argparse.ArgumentParser()

    parser.add_argument("flops_project_id", type=str)
    parser.add_argument(
        "mqtt_ip",
        type=str,
        help="The MQTT IP to be able to notify the FLOps manager.",
    )
    parser.add_argument("project_observer_ip", type=str)

    parser.add_argument("aggregator_ip", type=str)
    parser.add_argument("data_tags", type=str)

    args = parser.parse_args()

    data_tags = args.data_tags.split(",")

    LearnerContext(
        flops_project_id=args.flops_project_id,
        mqtt_ip=args.mqtt_ip,
        project_observer_ip=args.project_observer_ip,
        aggregator_ip=args.aggregator_ip,
        data_tags=data_tags,
    )
