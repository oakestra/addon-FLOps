# Note: We need a separate var for the repo due to max line length linting.
_mnist_sklearn_ml_repo = "https://github.com/Malyuk-A/flops_ml_repo_mnist_sklearn"
_cifar10_keras_ml_repo = "https://github.com/Malyuk-A/flops_ml_repo_cifar10_keras"

DEVEL_BASE_IMAGES_MAPPING = {
    _mnist_sklearn_ml_repo: "ghcr.io/malyuk-a/mnist_sklearn_base_image:latest",
    _cifar10_keras_ml_repo: "ghcr.io/malyuk-a/cifar10_keras_base_image:latest",
    # Note: Simply add more entries if need be.
}
