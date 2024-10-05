import flwr_datasets
from flops_utils.logging import logger
from mock_data_provider.context import get_context
from mock_data_provider.data_sender import send_data_to_ml_data_server


def load_and_send_data_to_server() -> None:
    logger.info("Start loading dataset")

    # NOTE/TODO/Future Work
    #
    # Currently we are only loading the training part of the data not the test part.
    # Because we currently do not differentiate between test and training data.
    # As far as I know the partition_type needs to be provided and has to be
    # either "train" or "test"
    #
    # Later in the learner the dataset gets fetched and split up into train and test set.
    # Which is not the best because we currently do not consider/use the original test set at all
    # and split the original train set into train and test.
    #
    # We could fetch both the train and test, merge them and push them to get a larger dataset.
    partition_type = "train"

    federated_dataset = flwr_datasets.FederatedDataset(
        dataset=get_context().dataset_name,
        partitioners={partition_type: get_context().number_of_partitions},
    )

    logger.info("Finished loading dataset")

    for partition_number in range(get_context().number_of_partitions):
        partition = federated_dataset.load_partition(
            partition_number,
            partition_type,
        ).with_format("arrow")
        send_data_to_ml_data_server(partition)

    logger.info("Finished sending partitions")
