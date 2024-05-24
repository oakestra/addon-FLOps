import tempfile

import datasets
import pyarrow as pa
import pyarrow.parquet as pq
from flops_utils.env_vars_checker.py import get_env_var
from flops_utils.logging import logger

ML_DATA_SERVER_PORT = get_env_var("DATA_MANAGER_PORT", 11027)
# TODO remove hardcode
ML_DATA_SERVER_IP = get_env_var("ML_DATA_SERVER_IP", "192.168.178.44")


def send_data_to_ml_data_server(dataset: datasets.Dataset):
    """Note: The dataset should use the Arrow format.
    (This is not an absolute necessity, but uniformity reduces the risk of side effects.)
    """

    logger.info("Start sending data")
    client = pa.flight.connect(f"grpc://{ML_DATA_SERVER_IP}:{ML_DATA_SERVER_PORT}")

    with tempfile.NamedTemporaryFile() as tmp_file:
        dataset.to_parquet(tmp_file)
        # Note: Temporary files are buffers and ensure the content is properly propagated
        # to disk we need to flush when writing to them.
        tmp_file.flush()
        # TODO figure out naming convention, etc.
        upload_descriptor = pa.flight.FlightDescriptor.for_path("uploaded.parquet")
        schema = pa.parquet.read_schema(tmp_file)

        # Stream the Parquet file to the server.
        writer, _ = client.do_put(upload_descriptor, schema)
        writer.write_table(pq.read_table(tmp_file))
        writer.close()

    logger.info("Finished sending data")
