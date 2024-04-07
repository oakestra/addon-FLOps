from http import HTTPStatus

from flops.utils import notify_ui


class RootFLManagerException(Exception):
    def __init__(
        self,
        msg: str,
        http_status: HTTPStatus = None,
        flops_process_id: str = "",
    ):
        self.msg = msg
        self.http_status = http_status
        self.flops_process_id = flops_process_id

    def try_to_notify_ui(self):
        if self.flops_process_id:
            notify_ui(self.msg, self.flops_process_id)


class ImageBuilderException(RootFLManagerException):
    pass


class FlAggregatorException(RootFLManagerException):
    pass


class FLUIException(RootFLManagerException):
    pass


class MQTTException(RootFLManagerException):
    pass


class ImageRegistryException(RootFLManagerException):
    pass


class LoginException(RootFLManagerException):
    pass


class AppCreationException(RootFLManagerException):
    pass


class AppDeletionException(RootFLManagerException):
    pass


class AppFetchException(RootFLManagerException):
    pass


class ServiceDeploymentException(RootFLManagerException):
    pass
