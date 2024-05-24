import base64
import os
import tempfile

import datasets
import pyarrow
import pyarrow as pa
import pyarrow.dataset as ad
import pyarrow.flight
import pyarrow.parquet as pq
import requests
from flops_utils.logging import logger
from icecream import ic
from mock_data_provider.utils.env_vars import DATA_MANAGER_IP

ML_DATA_MANAGER_PORT = os.environ.get("DATA_MANAGER_PORT", 11027)


def send_data_to_data_manager(dataset_partition: datasets.Dataset):
    logger.info("Start sending data")
    # table = pyarrow.Table.from_pandas(dataset_partition.to_pandas())
    # with pyarrow.BufferOutputStream() as sink:
    #     pq.write_table(table, sink)
    #     buffer = sink.getvalue()
    # encoded_data = base64.b64encode(buffer)

    # url = f"http://{DATA_MANAGER_IP}:11027/api/data/binaries"
    # headers = {"Content-Type": "application/octet-stream"}
    # response = requests.post(url, data=encoded_data, headers=headers, verify=False)
    # print(response)

    # client = pa.flight.connect(f"grpc://0.0.0.0:{ML_DATA_MANAGER_PORT}")
    client = pa.flight.connect(f"grpc://192.168.178.44:{ML_DATA_MANAGER_PORT}")

    ic(type(dataset_partition))
    # table = ad.dataset([dataset_partition]).to_table()
    # table = dataset_partition.to_parquet()

    # with tempfile.TemporaryFile() as tmp:
    # pq.write_table(table, tmp)
    with tempfile.NamedTemporaryFile() as f:
        ic(f)
        ic(f.name)

        dataset_partition.to_parquet(f)
        # Note: Temporariy files are buffers and to make sure the content is properly propagated to disk we need to flush when writing to them.
        f.flush()
        # Encode the filename as bytes
        # upload_filename = f.name.encode("utf-8")

        # Create a FlightDescriptor for your Parquet file
        # upload_descriptor = pa.flight.FlightDescriptor.for_path("file.parquet")
        # upload_descriptor = pa.flight.FlightDescriptor.for_path(upload_filename)
        upload_descriptor = pa.flight.FlightDescriptor.for_path("uploaded.parquet")

        # Get the schema of the Parquet file
        # schema = pa.parquet.read_schema(upload_filename)
        schema = pa.parquet.read_schema(f)
        ic(schema)

        # Stream the Parquet file to the server
        writer, _ = client.do_put(upload_descriptor, schema)
        writer.write_table(pq.read_table(f))
        writer.close()

    logger.info("Finished sending data")
