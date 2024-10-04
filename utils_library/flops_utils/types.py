import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


# These flavors are a subset of MLflow's model flavors.
# They are used to decide which MLflow model flavor to use.
# https://mlflow.org/docs/latest/models.html#built-in-model-flavors
class MLModelFlavor(str, enum.Enum):
    SKLEARN = "sklearn"  # Scikit-learn
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    # This list can be further expanded.


class FLOpsMode(str, enum.Enum):
    CLASSIC = "classic"
    HIERARCHICAL = "hierarchical"


class PlatformSupport(str, enum.Enum):
    LINUX_AMD64 = "linux/amd64"
    LINUX_ARM64 = "linux/arm64"


class AggregatorType(enum.Enum):
    CLASSIC_AGGREGATOR = "CLASSIC_AGGREGATOR"

    ROOT_AGGREGATOR = "ROOT_AGGREGATOR"
    CLUSTER_AGGREGATOR = "CLUSTER_AGGREGATOR"
