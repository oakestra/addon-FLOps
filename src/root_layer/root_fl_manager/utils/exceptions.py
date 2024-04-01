from http import HTTPStatus

from fl_ui_management.notification import notify_ui
from flops.identifier import FlOpsIdentifier


class RootFLManagerException(Exception):
    def __init__(
        self,
        msg: str,
        http_status: HTTPStatus = None,
        flops_identifier: FlOpsIdentifier = None,
    ):
        self.msg = msg
        self.http_status = http_status
        self.flops_identifier = flops_identifier

    def try_to_notify_ui(self):
        if self.flops_identifier:
            notify_ui(self.msg, self.flops_identifier)


class ImageBuilderException(RootFLManagerException):
    pass


class FLUIException(RootFLManagerException):
    pass


class OakestraException(RootFLManagerException):
    pass


class MQTTException(RootFLManagerException):
    pass


class ImageRegistryException(RootFLManagerException):
    pass


class LoginException(RootFLManagerException):
    pass
