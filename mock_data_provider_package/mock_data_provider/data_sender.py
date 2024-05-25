import tempfile

import datasets
import pyarrow.flight as flight
import pyarrow.parquet as parquet
from flops_utils.env_vars import DOCKER_HOST_IP_LINUX, get_env_var
from flops_utils.logging import logger
from mock_data_provider.context import get_context
from mock_data_provider.utils.hash import generate_unique_hash_identifier

ML_DATA_SERVER_PORT = get_env_var("DATA_MANAGER_PORT", 11027)
ML_DATA_SERVER_IP = get_env_var("ML_DATA_SERVER_IP", DOCKER_HOST_IP_LINUX)


def send_data_to_ml_data_server(dataset: datasets.Dataset):
    """Note: The dataset should use the Arrow format.
    (This is not an absolute necessity, but uniformity reduces the risk of side effects.)
    """

    logger.info("Start sending data")
    client = flight.connect(f"grpc://{ML_DATA_SERVER_IP}:{ML_DATA_SERVER_PORT}")

    with tempfile.NamedTemporaryFile() as tmp_file:
        dataset.to_parquet(tmp_file)
        # Note: Temporary files are buffers and ensure the content is properly propagated
        # to disk we need to flush when writing to them.
        tmp_file.flush()

        unique_file_name = (
            f"{get_context().data_tag}.{generate_unique_hash_identifier(tmp_file.name)}"
        )

        final_file_name = f"{unique_file_name}.parquet"
        upload_descriptor = flight.FlightDescriptor.for_path(final_file_name)
        schema = parquet.read_schema(tmp_file.name)

        # Stream the Parquet file to the server.
        writer, _ = client.do_put(upload_descriptor, schema)
        writer.write_table(parquet.read_table(tmp_file.name))
        writer.close()

    logger.info(f"Finished sending data. Stored data as '{final_file_name}'")
