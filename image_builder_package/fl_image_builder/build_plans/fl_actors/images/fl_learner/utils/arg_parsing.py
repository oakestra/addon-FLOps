import argparse
from typing import List, Tuple

from context import LearnerContext


def parse_args() -> Tuple[str, List[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("aggregator_ip", type=str)
    parser.add_argument("data_tags", type=str)

    args = parser.parse_args()

    data_tags = args.data_tags.split(",")

    LearnerContext(
        aggregator_ip=args.aggregator_ip,
        data_tags=data_tags,
    )
