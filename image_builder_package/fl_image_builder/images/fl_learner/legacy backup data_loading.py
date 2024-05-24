import base64
import pathlib
import tempfile
import zipfile
from io import BytesIO

import pandas
import pyarrow
import pyarrow.parquet as pq
import requests
from datasets import Dataset
from flops_utils.logging import logger
from icecream import ic

# Note: "localhost" does not work.
DOCKER_HOST_IP_LINUX = "172.17.0.1"


def load_data_from_worker_node():  # -> TODO
    try:
        response = requests.get(
            f"http://{DOCKER_HOST_IP_LINUX}:11027/api/data/binaries"
        )
        ic(response)
        # Check if the request was successful
        if response.status_code == 200:
            # Create a temporary directory to store the unzipped files
            temp_dir = pathlib.Path(tempfile.mkdtemp())

            # Open the ZIP file in read-binary mode
            received_zip_path = temp_dir / "received.zip"
            with open(received_zip_path, "wb") as f:
                f.write(response.content)

            # Unzip the received ZIP file
            with zipfile.ZipFile(received_zip_path, "r") as zip_ref:
                zip_ref.extractall(path=temp_dir)

            received_zip_path.unlink()

            files_in_dir = [item for item in temp_dir.iterdir() if item.is_file()]

            for binary_file in files_in_dir:
                with open(binary_file, "rb") as file:
                    binary_data = file.read()

                # Step 2: Decode the Base64 encoded data
                decoded_data = base64.b64decode(binary_data)

                # # Step 3: Convert bytes to PyArrow Table using BufferReader
                # with pyarrow.memory_map(decoded_data) as memmap:
                #     table = pyarrow.ipc.open_file(memmap).read_all()
                # Instead of using memory_map, use BytesIO to avoid potential stdout issues
                # memmap = BytesIO(decoded_data)
                # table = pyarrow.ipc.open_file(memmap).read_all()

                # Directly create a PyArrow Table from the decoded data
                table = pyarrow.Table.from_pandas(pandas.DataFrame(decoded_data))

                # Step 4: Convert PyArrow Table to Pandas DataFrame
                df = table.to_pandas()

                # Step 5: Create Arrow Dataset
                dataset = Dataset.from_pandas(df)
                ic(type(dataset))
                ic(dataset)

            logger.info(f"Files extracted successfully to {temp_dir}")
        else:
            logger.error(f"Error: Received status code {response.status_code}.")
    except Exception:
        logger.exception("An unexpected exception occurred.")


# def recover_dataset_from_binary():
#     binary_file_path = f"{DATA_VOLUME}/{current_time}.bin"

#     with open(binary_file_path, "rb") as file:
#         binary_data = file.read()

#     # Step 2: Decode the Base64 encoded data
#     decoded_data = base64.b64decode(binary_data)

#     # Step 3: Convert bytes to PyArrow Table
#     table = pyarrow.Table.from_buffer(decoded_data)

#     # Step 4: Convert PyArrow Table to Pandas DataFrame
#     df = table.to_pandas()

#     # Step 5: Create Arrow Dataset
#     dataset = Dataset.from_pandas(df)

#     return dataset
