import os
import tempfile

import datasets
import pyarrow.flight as flight
import pyarrow.parquet as parquet

# Note: "localhost" does not work.
DOCKER_HOST_IP_LINUX = "172.17.0.1"


def load_data_from_ml_data_server() -> datasets.Dataset:
    """Loads the data from the co-located ml-data-server from the learner node.

    Returns a single dataset that encompasses all matching found data from the server.
    This dataset is in "Arrow" format.
    """

    client = flight.connect("grpc://192.168.178.44:11027")
    descriptor = flight.FlightDescriptor.for_path("uploaded.parquet")
    flight_info = client.get_flight_info(descriptor)
    reader = client.do_get(flight_info.endpoints[0].ticket)
    arrow_table = reader.read_all()

    # Note/Important/Future-Work
    # The current solution is a workaround that can be optimized.
    #
    # We have the following challenge here:
    #
    # We get a table of type <class 'pyarrow.lib.Table'> back from the reader.
    # We currently convert this table and save it as a tmp parquet file.
    # Then we use the datasets library to reconstruct our original dataset object
    # from this parquet file.
    #
    # Note that the received table and the final dataset are both in arrow format.
    #
    # We should find a way to remove the intermediate parquet transformation/storage step.
    # This step is currently used because directly transforming the table
    # into a dataset is not possible (as far as we know).
    # This table needs to be converted into a dataset via pandas.
    # Here the complex underlying data structure gets misinterpreted.
    # Resulting in a wrong final shape of our data.

    # Using the tmpfile lib leads to unexpected errors here, because the tmpfiles are not real files
    # They lead to specific type related issues or lack certain methods.
    # with tempfile.NamedTemporaryFile(mode="wb") as tmp_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".parquet") as tmp_file:
        parquet.write_table(arrow_table, tmp_file.name)
        tmp_file.flush()

    # Note: We need to split up the read and write part
    # because the writing has to occur in binary mode but not the reading.
    dataset = datasets.Dataset.from_parquet(tmp_file.name).with_format("arrow")
    os.remove(tmp_file.name)

    return dataset
