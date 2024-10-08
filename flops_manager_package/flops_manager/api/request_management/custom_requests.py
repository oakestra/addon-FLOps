import json
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, NamedTuple, Optional

import requests
from flops_manager.api.request_management.custom_http import HttpMethods
from flops_manager.api.utils.login import get_login_token
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_utils.logging import colorful_logger as logger


class RequestCore(NamedTuple):
    base_url: str
    api_endpoint: str = ""
    query_params: str = ""
    http_method: HttpMethods = HttpMethods.GET
    custom_headers: Optional[dict] = None
    data: Optional[dict] = None


class RequestAuxiliaries(NamedTuple):
    what_should_happen: str
    flops_exception_type: FlOpsExceptionTypes = FlOpsExceptionTypes.UNSPECIFIED
    show_msg_on_success: bool = False
    is_oakestra_api: bool = True
    flops_project_id: str = ""


# NOTE: The use of Pydantic here leads to strange validation errors.
@dataclass
class CustomRequest:
    core: RequestCore
    aux: RequestAuxiliaries

    headers: Optional[dict] = field(default=None, init=False)
    url: str = field(default="", init=False)
    args: Optional[dict] = field(default=None, init=False)
    response: Optional[requests.Response] = field(default=None, init=False)

    def __post_init__(self):
        self._prepare()

    def _prepare(self) -> None:
        self.url = self.core.base_url
        if self.core.api_endpoint is not None:
            self.url = f"{self.core.base_url}{self.core.api_endpoint}"
        if self.core.query_params is not None:
            self.url += f"?{self.core.query_params}"

        if self.core.custom_headers:
            self.headers = self.core.custom_headers
        else:
            self.headers = (
                {"Authorization": f"Bearer {get_login_token()}"} if self.aux.is_oakestra_api else {}
            )

        if self.core.data and not self.core.custom_headers:
            self.headers["Content-Type"] = "application/json"

        self.args = {
            "url": self.url,
            "verify": False,
            **({"headers": self.headers} if self.headers else {}),
            **({"json": self.core.data} if self.core.data else {}),
        }

    def _create_failure_msg(self) -> str:
        return " ".join(
            (
                self.aux.what_should_happen,
                "request failed",
                f"with {self.response.status}" if self.response else "- no response",
                f"for '{self.core.http_method}' '{self.url}",
            )
        )

    def execute(self) -> Any:
        error_msg = ""
        try:
            self.response = self.core.http_method.call(**self.args)
            self.response.status = HTTPStatus(self.response.status_code)
            if self.response.status == HTTPStatus.OK:
                if self.aux.show_msg_on_success:
                    logger.info(f"Success: '{self.aux.what_should_happen}'")
                response = self.response.json()
                if isinstance(response, str):
                    response = json.loads(response)
                return response

        except requests.exceptions.RequestException as e:
            error_msg = f"exception: {e}: "

        error_msg += self._create_failure_msg()

        raise FLOpsManagerException(
            flops_exception_type=self.aux.flops_exception_type,
            flops_project_id=self.aux.flops_project_id,
            text=error_msg,
            http_status=self.response.status if self.response else None,
        )
