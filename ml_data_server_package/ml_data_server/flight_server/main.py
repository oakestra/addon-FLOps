# Reference: https://arrow.apache.org/cookbook/py/flight.html#id3

import json
import os
import pathlib

import pyarrow
import pyarrow.flight as flight
import pyarrow.parquet as parquet

ML_DATA_MANAGER_PORT = os.environ.get("DATA_MANAGER_PORT", 11027)
DATA_VOLUME = pathlib.Path("/ml_data_server_volume")


class FlightServer(flight.FlightServerBase):

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
        schema = parquet.read_schema(dataset_path)
        metadata = parquet.read_metadata(dataset_path)
        descriptor = flight.FlightDescriptor.for_path(dataset.encode("utf-8"))
        endpoints = [flight.FlightEndpoint(dataset, [self._location])]
        return flight.FlightInfo(
            schema, descriptor, endpoints, metadata.num_rows, metadata.serialized_size
        )

    def list_flights(self, context, criteria):
        requested_data_tags = json.loads(criteria.decode("utf-8"))["data_tags"]
        for dataset in self._repo.iterdir():
            if dataset.name.split(".")[0] in requested_data_tags:
                # NOTE: Returns a generator object that can be iterated over via a for loop.
                yield self._make_flight_info(dataset.name)

    def get_flight_info(self, context, descriptor):
        return self._make_flight_info(descriptor.path[0].decode("utf-8"))

    def do_put(self, context, descriptor, reader, writer):
        dataset = descriptor.path[0].decode("utf-8")
        dataset_path = self._repo / dataset
        # Read the uploaded data and write to Parquet incrementally
        with dataset_path.open("wb") as sink:
            with parquet.ParquetWriter(sink, reader.schema) as writer:
                for chunk in reader:
                    writer.write_table(pyarrow.Table.from_batches([chunk.data]))

    def do_get(self, context, ticket):
        dataset = ticket.ticket.decode("utf-8")
        # Stream data from a file
        dataset_path = self._repo / dataset
        reader = parquet.ParquetFile(dataset_path)
        return flight.GeneratorStream(reader.schema_arrow, reader.iter_batches())

    def list_actions(self, context):
        return [
            ("drop_dataset", "Delete a dataset."),
        ]

    def do_action(self, context, action):
        if action.type == "drop_dataset":
            self.do_drop_dataset(action.body.to_pybytes().decode("utf-8"))
        else:
            raise NotImplementedError

    def do_drop_dataset(self, dataset):
        dataset_path = self._repo / dataset
        dataset_path.unlink()


def handle_server() -> None:
    server = FlightServer()
    server._repo.mkdir(exist_ok=True)
    server.serve()
