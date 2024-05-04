# Note: This wrapper is used to handle ml repo files
# which get injected during the image build.
# I.e. these files are not yet present.
# Additionally it handles exceptions and helps linters, etc to work normally.

import sys

from flops_utils.logging import logger

try:
    from model_manager import ModelManager  # type: ignore

    ModelManager = ModelManager
except ImportError:
    logger.exception("A ML repo file was not found.")
    sys.exit(1)
