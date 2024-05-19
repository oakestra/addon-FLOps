# Note: This wrapper is used to provide ML repo developers/users with mock FLOps Learner components.
# E.g. The ML repo developer does not have access to any data of the worker nodes yet.
# This data will be fetched by the Learner's data_loading from the Data Manager Sidecar.
# This data_loading is part of the Learner image and should be abstracted away from the ML repo.
# To be able to include the data_loading methods in the ML repo code these mocks are provided.
# These mocks will be replaced with the real implementation during the FLOps image build process.

import sys

from flops_utils.logging import logger


def load_ml_data():
    try:
        from data_loading import load_data_from_worker_node  # type: ignore

        return load_data_from_worker_node()
    except ImportError:
        logger.exception("The data_loading file was not found.")
        sys.exit(1)
