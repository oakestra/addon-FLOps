import hashlib
import pathlib

import pyarrow.parquet as parquet


def generate_unique_hash_identifier(parquet_file_path: pathlib.Path) -> str:
    arrow_table = parquet.read_table(parquet_file_path)
    data_frame = arrow_table.to_pandas()
    # Note: This approach might need adjustments for very large datasets
    stringified_data_frame = "".join(
        data_frame.astype(str).applymap(lambda x: str(x)).values.flatten().tolist()
    )
    return hashlib.md5(stringified_data_frame.encode()).hexdigest()
