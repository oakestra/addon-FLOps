# Used to abstract away concrete uses of MLflow model flavors.
# Based on the provided flavor from the FLOps SLA the specific MLflow model flavor will be used.

import os
import sys

from flops_utils.logging import logger
from flops_utils.types import MLModelFlavor


def get_ml_model_flavor():
    match MLModelFlavor(os.environ.get("ML_MODEL_FLAVOR")):
        case MLModelFlavor.KERAS:
            import mlflow.keras

            return mlflow.keras
        case MLModelFlavor.PYTORCH:
            import mlflow.pytorch

            return mlflow.pytorch

        case MLModelFlavor.SKLEARN:
            import mlflow.sklearn

            return mlflow.sklearn
        case _:
            logger.exception("Provided MLModelFlavor is not supported yet.")
            sys.exit(1)
