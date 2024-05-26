import flwr_datasets
from datasets import Dataset
from flops_utils.logging import logger
from mock_data_provider.context import get_context


def load_data() -> Dataset:
    logger.info("Start loading data")

    # Note/TODO/Future Work
    #
    # Currently we are only loading the training part of the data not the test part.
    # Because we currently do not differentiate between test and training data.
    # As far as I know the partition_type needs to be provided and has to be
    # either "train" or "test"
    #
    # Later in the learner the dataset gets fetched and split up into train and test set.
    # Which is not the best because we currently do not consider/use the original test set at all
    # and split the original train set into train and test!
    #
    # We could fetch both the train and test, merge them and push them to get a larger dataset.
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
