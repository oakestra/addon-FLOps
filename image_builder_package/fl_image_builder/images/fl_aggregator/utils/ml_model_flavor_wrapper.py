# Used to abstract away concrete uses of flavors.
# Based on the provided flavor from the FLOps SLA the specific mlflow model flavor will be used.

import os

from flops_utils.types import MLModelFlavor

match MLModelFlavor(os.environ.get("ML_MODEL_FLAVOR")):
    case MLModelFlavor.KERAS:
        import mlflow.keras

        mlflow_model_flavor = mlflow.keras
