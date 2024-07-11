# NOTE: We need a separate var for the repo due to max line length linting.
_mnist_sklearn_ml_repo = "https://github.com/Malyuk-A/flops_ml_repo_mnist_sklearn"
_cifar10_keras_ml_repo = "https://github.com/Malyuk-A/flops_ml_repo_cifar10_keras"
_cifar10_pytorch_ml_repo = "https://github.com/Malyuk-A/flops_ml_repo_cifar10_pytorch"

DEVEL_BASE_IMAGES_MAPPING = {
    _mnist_sklearn_ml_repo: "ghcr.io/oakestra/addon-flops/baseimage-mnist-sklearn:latest",
    _cifar10_keras_ml_repo: "ghcr.io/oakestra/addon-flops/baseimage-cifar10-keras:latest",
    _cifar10_pytorch_ml_repo: "ghcr.io/oakestra/addon-flops/baseimage-cifar10-pytorch:latest",
}
