# flops-utils
This package/library contains common pieces of code for the [FLOps project](https://github.com/oakestra/addon-FLOps?tab=readme-ov-file).


## User Facing Features

flops-utils provides FLOPs users with guiding abstract template classes for implementing their ML models and "proxy/place-holder" components to satisfy linters.

When FLOps users want to structure their ML code to match the structural requirements of FLOps they should do the following:

```Python
# data_manager.py

from flops_utils.ml_repo_building_blocks import load_dataset
from flops_utils.ml_repo_templates import DataManagerTemplate

class DataManager(DataManagerTemplate):
    def __init__(self):
        ... = self._prepare_data()

    def _prepare_data(self, partition_id=1) -> Any:
        dataset = load_dataset()
        ...
        return ...

    def get_data(self) -> Tuple[Any, Any]:
        return ...

```

```Python
# model_manager.py

import warnings
from typing import Any, Tuple

import numpy as np
from data_manager import DataManager
from flops_utils.ml_repo_templates import ModelManagerTemplate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss


class ModelManager(ModelManagerTemplate):
    def __init__(self):
        self.model = ...
        self._set_init_params()

    def _set_init_params(self) -> None:
        ...

    def set_model_data(self) -> None:
        ... = DataManager().get_data()

    def get_model(self) -> Any:
        return self.model

    def get_model_parameters(self) -> Any:
        params = ...
        return params

    def set_model_parameters(self, parameters) -> None:
        ...

    def fit_model(self) -> int:
        return len(self.x_train)

    def evaluate_model(self) -> Tuple[Any, Any, int]:
        loss = ...
        accuracy = ...
        return loss, accuracy, len(self.x_test)
        
```

A tangible example implementation is available [here](https://github.com/Malyuk-A/flops_ml_repo_mnist_sklearn/tree/main).

## Internal FLOps Commonalities
- Logger
- Types
- MQTT Topics
- Handlers
    - Notifications (Project Observer & FLOps Manager)
    - Environment Variables
- Auxiliary Constructs
    - Running Shell Commands
    - Measuring Execution Time Frames

## Installation Alternatives

One can also include and use these utilities by doing the following:
```
pip install --no-cache-dir git+https://github.com/oakestra/addon-FLOps.git@main#subdirectory=utils_library
```
