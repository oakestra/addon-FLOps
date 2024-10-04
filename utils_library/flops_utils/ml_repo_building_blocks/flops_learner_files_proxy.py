# Note: This proxy is used to provide ML repo developers/users with stub FLOps Learner components.
# E.g. The ML repo developer does not have access to any data of the worker nodes yet.
# This data will be fetched by the Learner's data_loading from the Data Manager Sidecar.
# This data_loading is part of the Learner image and should be abstracted away from the ML repo.
# To be able to include the data_loading methods in the ML repo code these mocks are provided.
# These mocks will be replaced with the real implementation during the FLOps image build process.

import sys

import datasets  # type: ignore

from flops_utils.logging import logger


def load_dataset() -> datasets.Dataset:
    """Loads the data from the co-located ml-data-server from the learner node.

    Returns a single dataset that encompasses all matching found data from the server.
    This dataset is in "Arrow" format.
    """

    try:
        from data_loading import load_data_from_ml_data_server  # type: ignore

        return load_data_from_ml_data_server()
    except ImportError:
        logger.exception("The data_loading file was not found.")
        sys.exit(1)
