from dataclasses import dataclass, field
from http import HTTPStatus

from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_utils.logging import colorful_logger as logger


# NOTE: Pydantic.BaseModel and Exception do not seem to work well if inherited together.
@dataclass
class FLOpsManagerException(Exception):
    flops_exception_type: FlOpsExceptionTypes
    text: str
    http_status: HTTPStatus = None
    message: str = field(default="<message is not set>", init=False)
    flops_project_id: str = None

    def __post_init__(self) -> None:
        self.message = f"'{self.flops_exception_type}' exception occured: {self.text}"

    def log(self) -> None:
        logger.exception(f"{self.message}, {self.http_status}")
