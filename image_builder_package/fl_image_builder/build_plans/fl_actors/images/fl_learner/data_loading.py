import json
import pathlib
import shutil
import tempfile

import datasets
import pyarrow
import pyarrow.flight as flight
import pyarrow.parquet as parquet
from context import get_context

# NOTE: "localhost" does not work.
from flops_utils.env_vars import DOCKER_HOST_IP_LINUX
from flops_utils.logging import logger
from notification_management import notify_about_failure_and_terminate


def load_data_from_ml_data_server() -> datasets.Dataset:
    """Loads the data from the co-located ml-data-server from the learner node.

    Returns a single dataset that encompasses all matching found data from the server.
    This dataset is in "Arrow" format.
    """

    logger.info("Start loading data from ML Data Server")

    client = flight.connect(f"grpc://{DOCKER_HOST_IP_LINUX}:11027")
    criteria = {"data_tags": get_context().data_tags}
    # NOTE: The Server endpoint expects binary data.
    flights = client.list_flights(criteria=json.dumps(criteria).encode("utf-8"))

    tmp_dir_path = pathlib.Path(tempfile.mkdtemp())

    for _flight in flights:
        reader = client.do_get(_flight.endpoints[0].ticket)
        arrow_table = reader.read_all()

        # NOTE/Important/Future-Work
        # The current solution is a workaround that can be optimized.
        #
        # We have the following challenge here:
        #
        # We get a table of type <class 'pyarrow.lib.Table'> back from the reader.
        # We currently convert this table and save it as a tmp parquet file.
        # Then we use the datasets library to reconstruct our original dataset object
        # from this parquet file.
        #
        # NOTE: that the received table and the final dataset are both in arrow format.
        #
        # We should find a way to remove the intermediate parquet transformation/storage step.
        # This step is currently used because directly transforming the table
        # into a dataset is not possible (as far as we know).
        # This table needs to be converted into a dataset via pandas.
        # Here the complex underlying data structure gets misinterpreted.
        # Resulting in a wrong final shape of our data.

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".parquet",
            dir=tmp_dir_path,
        ) as tmp_file:
            parquet.write_table(arrow_table, tmp_file.name)
            tmp_file.flush()

    number_of_downloaded_files = len(list(tmp_dir_path.glob("*")))
    logger.info(f"Found and downloaded '{number_of_downloaded_files}' flights/files")
    if number_of_downloaded_files == 0:
        notify_about_failure_and_terminate(
            context=get_context(),
            error_msg=f"No matching data found for provided data tags '{get_context().data_tags}'",
        )

    parquet_tables = []
    for file_name in tmp_dir_path.iterdir():
        parquet_tables.append(parquet.read_table(file_name))

    merged_parquet_path = tmp_dir_path / "merged.parquet"
    parquet.write_table(pyarrow.concat_tables(parquet_tables), merged_parquet_path)
    dataset = datasets.Dataset.from_parquet(str(merged_parquet_path)).with_format("arrow")
    shutil.rmtree(tmp_dir_path)
    logger.info("Successfully created (merged) dataset")
    return dataset
