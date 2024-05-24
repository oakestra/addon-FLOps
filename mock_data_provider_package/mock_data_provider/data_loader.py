import random

import flwr_datasets
from datasets import Dataset
from flops_utils.logging import logger
from flwr_datasets import FederatedDataset


def load_data(
    hugging_face_dataset: str = "mnist",
    seed: int = None,
) -> Dataset:
    logger.info("Start loading data")

    # partition_type = "train"

    # if seed:
    #     random.seed(seed)

    # total_partitions = random.randint(1, 10)
    # federated_dataset = flwr_datasets.FederatedDataset(
    #     dataset=hugging_face_dataset, partitioners={partition_type: total_partitions}
    # )
    # selected_partition = random.randint(1, total_partitions)
    # partition = federated_dataset.load_partition(
    #     selected_partition - 1, partition_type
    # ).with_format("arrow")

    fds = FederatedDataset(dataset="mnist", partitioners={"train": 3})
    dataset = fds.load_partition(1, "train").with_format("numpy")

    logger.info("Finished loading data")
    # return partition
    return dataset
