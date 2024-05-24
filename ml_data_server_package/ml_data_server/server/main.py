# Reference: https://arrow.apache.org/cookbook/py/flight.html#id3

import os
import pathlib

import pyarrow as pa
import pyarrow.flight
import pyarrow.parquet
from icecream import ic

ML_DATA_MANAGER_PORT = os.environ.get("DATA_MANAGER_PORT", 11027)
DATA_VOLUME = pathlib.Path("/flops_data_manager_sidecar_volume")


class FlightServer(pa.flight.FlightServerBase):

    def __init__(
        self,
        location=f"grpc://0.0.0.0:{ML_DATA_MANAGER_PORT}",
        repo=pathlib.Path(DATA_VOLUME),
        **kwargs,
    ):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

    def _make_flight_info(self, dataset):
        dataset_path = self._repo / dataset
        schema = pa.parquet.read_schema(dataset_path)
        metadata = pa.parquet.read_metadata(dataset_path)
        descriptor = pa.flight.FlightDescriptor.for_path(dataset.encode("utf-8"))
        endpoints = [pa.flight.FlightEndpoint(dataset, [self._location])]
        return pyarrow.flight.FlightInfo(
            schema, descriptor, endpoints, metadata.num_rows, metadata.serialized_size
        )

    def list_flights(self, context, criteria):
        ic("list_flights")
        for dataset in self._repo.iterdir():
            yield self._make_flight_info(dataset.name)

    def get_flight_info(self, context, descriptor):
        ic("get_flight_info")
        return self._make_flight_info(descriptor.path[0].decode("utf-8"))

    def do_put(self, context, descriptor, reader, writer):
        ic("do_put")
        dataset = descriptor.path[0].decode("utf-8")
        dataset_path = self._repo / dataset
        # Read the uploaded data and write to Parquet incrementally
        with dataset_path.open("wb") as sink:
            with pa.parquet.ParquetWriter(sink, reader.schema) as writer:
                for chunk in reader:
                    writer.write_table(pa.Table.from_batches([chunk.data]))

    def do_get(self, context, ticket):
        ic("do_get")
        dataset = ticket.ticket.decode("utf-8")
        # Stream data from a file
        dataset_path = self._repo / dataset
        reader = pa.parquet.ParquetFile(dataset_path)
        return pa.flight.GeneratorStream(reader.schema_arrow, reader.iter_batches())

    def list_actions(self, context):
        ic("list_actions")
        return [
            ("drop_dataset", "Delete a dataset."),
        ]

    def do_action(self, context, action):
        ic("do_action")
        if action.type == "drop_dataset":
            self.do_drop_dataset(action.body.to_pybytes().decode("utf-8"))
        else:
            raise NotImplementedError

    def do_drop_dataset(self, dataset):
        dataset_path = self._repo / dataset
        dataset_path.unlink()


def handle_server() -> None:
    ic("Start Server")
    server = FlightServer()
    server._repo.mkdir(exist_ok=True)
    server.serve()
