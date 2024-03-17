import base64
import random

import flwr_datasets
import pyarrow
import pyarrow.parquet as pq
import requests

random.randint(1, 100)


def load_data(
    hugging_face_dataset: str = "cifar10",
    seed: int = None,
):
    partition_type = "train"

    if seed:
        random.seed(seed)

    total_partitions = random.randint(1, 10)
    federated_dataset = flwr_datasets.FederatedDataset(
        dataset=hugging_face_dataset, partitioners={partition_type: total_partitions}
    )
    selected_partition = random.randint(1, total_partitions)
    partition = federated_dataset.load_partition(selected_partition - 1, partition_type)
    return partition


def send_data_to_colocated_data_manager(dataset_partition):
    table = pyarrow.Table.from_pandas(dataset_partition.to_pandas())
    with pyarrow.BufferOutputStream() as sink:
        pq.write_table(table, sink)
        buffer = sink.getvalue()
    encoded_data = base64.b64encode(buffer)

    url = "https://localhost:11027/api/data/binaries"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=encoded_data, headers=headers, verify=False)
    print(response)


def main():
    dataset_partition = load_data()
    send_data_to_colocated_data_manager(dataset_partition)


if __name__ == "__main__":
    main()
