import flwr_datasets
from datasets import Dataset
from flops_utils.logging import logger
from mock_data_provider.context import get_context


def load_data() -> Dataset:
    logger.info("Start loading data")

    partition_type = "train"

    federated_dataset = flwr_datasets.FederatedDataset(
        dataset=get_context().dataset_name,
        partitioners={partition_type: get_context().number_of_partitions},
    )
    selected_partition = 1  # TODO
    partition = federated_dataset.load_partition(
        selected_partition - 1,
        partition_type,
    ).with_format("arrow")

    logger.info("Finished loading data")
    return partition
