import argparse

from mock_data_provider.context import MockDataProviderContext


def parse_args() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset_name", type=str)
    parser.add_argument("number_of_partitions", type=int, default=1)
    parser.add_argument("data_tag", type=str)

    args = parser.parse_args()

    MockDataProviderContext(
        dataset_name=args.dataset_name,
        number_of_partitions=args.number_of_partitions,
        data_tag=args.data_tag,
    )
