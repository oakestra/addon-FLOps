from http import HTTPStatus

from flops.fl_ui_management.notification import notify_ui
from flops.process import FlOpsProcess


class RootFLManagerException(Exception):
    def __init__(
        self,
        msg: str,
        http_status: HTTPStatus = None,
        flops_process: FlOpsProcess = None,
    ):
        self.msg = msg
        self.http_status = http_status
        self.flops_process = flops_process

    def try_to_notify_ui(self):
        if self.flops_process:
            notify_ui(self.msg, self.flops_process)


class ImageBuilderException(RootFLManagerException):
    pass


class FLUIException(RootFLManagerException):
    pass


class MQTTException(RootFLManagerException):
    pass


class ImageRegistryException(RootFLManagerException):
    pass


class LoginException(RootFLManagerException):
    pass
