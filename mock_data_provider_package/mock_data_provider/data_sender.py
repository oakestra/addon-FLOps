import base64

import pyarrow
import pyarrow.parquet as pq
import requests
from flops_utils.logging import logger
from mock_data_provider.utils.env_vars import DATA_MANAGER_IP


def send_data_to_data_manager(dataset_partition):
    logger.info("Start sending data")
    table = pyarrow.Table.from_pandas(dataset_partition.to_pandas())
    with pyarrow.BufferOutputStream() as sink:
        pq.write_table(table, sink)
        buffer = sink.getvalue()
    encoded_data = base64.b64encode(buffer)

    url = f"http://{DATA_MANAGER_IP}:11027/api/data/binaries"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=encoded_data, headers=headers, verify=False)
    print(response)
    logger.info("Finished sending data")
