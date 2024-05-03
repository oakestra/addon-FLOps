import argparse


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("flops_aggregator_ip", type=str)

    args = parser.parse_args()

    return args.flops_aggregator_ip
