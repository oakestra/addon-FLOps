from enum import Enum


# These flavors are a subset of MLflow's model flavors.
# They are used to decide which MLflow model flavor to use.
# https://mlflow.org/docs/latest/models.html#built-in-model-flavors
class MLModelFlavor(str, Enum):
    SKLEARN = "sklearn"  # Scikit-learn
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    # This list can be further expanded.
