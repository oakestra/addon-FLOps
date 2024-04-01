import json
from http import HTTPStatus
from typing import NamedTuple

import requests
from api.custom_http import HttpMethod
from api.login import get_login_token
from utils.exceptions import RootFLManagerException
from utils.identifier import FlOpsIdentifier
from utils.logging import logger


class RequestCore:
    def __init__(
        self,
        base_url: str,
        api_endpoint: str = None,
        query_params: str = None,
        http_method: HttpMethod = HttpMethod.GET,
        custom_headers: dict = None,
        data: dict = None,
    ):
        self.base_url = base_url
        self.api_endpoint = api_endpoint
        self.query_params = query_params
        self.http_method = http_method
        self.custom_headers = custom_headers
        self.data = data

    def __str__(self):
        return " ".join(
            (
                "RequestCore(",
                f"base_url={self.base_url}",
                f"api_endpoint={self.api_endpoint}",
                f"query_params={self.query_params}",
                f"http_method={self.http_method}",
                f"http_method={self.http_method}",
                f"data={self.data}",
                ")",
            )
        )


class RequestAuxiliaries(NamedTuple):
    what_should_happen: str
    exception: RootFLManagerException
    flops_identifier: FlOpsIdentifier = None
    show_msg_on_success: bool = False
    is_oakestra_api: bool = True


class CustomRequest:
    def __init__(self, core: RequestCore, aux: RequestAuxiliaries):
        self.core = core
        self.aux = aux
        self.headers = None
        self.url = None
        self.args = None
        self.response = None
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
                f"with {self.response.status}" if self.response else "entirely, i.e. no response",
                f"for '{self.core.http_method}' '{self.url}",
            )
        )

    def execute(self) -> any:
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

        raise self.aux.exception(
            msg=error_msg,
            http_status=self.response.status if self.response else None,
            flops_identifier=self.aux.flops_identifier,
        )
