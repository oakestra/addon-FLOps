from dataclasses import dataclass
from http import HTTPStatus

from flops.utils import notify_ui


# Note: Pydantic.BaseModel and Exception do not seem to work well if inherited together.
@dataclass
class RootFLManagerException(Exception):
    msg: str
    http_status: HTTPStatus = None
    flops_project_id: str = ""

    def try_to_notify_ui(self):
        if self.flops_project_id:
            notify_ui(msg=self.msg, flops_project_id=self.flops_project_id)


class ImageBuilderException(RootFLManagerException):
    pass


class FlAggregatorException(RootFLManagerException):
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


class FLOpsProjectServiceAppend(RootFLManagerException):
    pass


class ServiceDeploymentException(RootFLManagerException):
    pass


class ServiceUnDeploymentException(RootFLManagerException):
    pass
