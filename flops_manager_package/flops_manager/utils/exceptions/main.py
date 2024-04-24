from dataclasses import dataclass, field
from http import HTTPStatus

from flops_manager.utils.exceptions.types import FlOpsExceptionTypes


# Note: Pydantic.BaseModel and Exception do not seem to work well if inherited together.
@dataclass
class FLOpsManagerException(Exception):
    flops_exception_type: FlOpsExceptionTypes
    text: str
    http_status: HTTPStatus = None
    flops_project_id: str = None

    message: str = field(init=False)

    def model_post_init(self, _) -> None:
        self.message = f"'{self.flops_exception_type}' exception occured: {self.text}"
