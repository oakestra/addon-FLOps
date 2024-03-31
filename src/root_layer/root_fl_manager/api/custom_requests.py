import json
from http import HTTPStatus
from typing import NamedTuple

import requests
from api.custom_http import HttpMethod
from api.login import get_login_token
from icecream import ic
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

        ic("aa")
        self._prepare()
        ic("bb")
        self._execute()
        ic("cc")

    def _prepare(self) -> None:
        self.url = self.core.base_url
        if self.core.api_endpoint is not None:
            self.url = f"{self.core.base_url}{self.core.api_endpoint}"
        if self.core.query_params is not None:
            ic(self.core.query_params)
            self.url += f"?{self.core.query_params}"

        if self.core.custom_headers:
            self.headers = self.core.custom_headers
        else:
            self.headers = (
                {"Authorization": f"Bearer {get_login_token()}"} if self.aux.is_oakestra_api else {}
            )

        ic("13")
        if self.core.data and not self.core.custom_headers:
            self.headers["Content-Type"] = "application/json"

        ic("22")

        self.args = {
            "url": self.url,
            "verify": False,
            **({"headers": self.headers} if self.headers else {}),
            **({"json": self.core.data} if self.core.data else {}),
        }
        ic("33")

    def _create_failure_msg(self) -> str:
        return " ".join(
            (
                self.aux.what_should_happen,
                "request failed",
                f"with {self.response.status}" if self.response else "entirely, i.e. no response",
                f"for '{self.core.http_method}' '{self.url}",
            )
        )

    def _execute(self) -> any:
        error_msg = ""
        try:

            ic("aaaaaaaaaaaaaaa")
            ic(self.core.http_method)
            ic("aaaaa11111111111")
            ic(self.args)
            ic("aaaaa222222222")

            # self.response = self.core.http_method.call(**self.args)
            url = self.args["url"]
            _json = self.args["json"]
            headers = self.args["headers"]
            verify = self.args["verify"]
            ic(url, _json, headers, verify)

            test_json = {
                "sla_version": "v2.0",
                "customerID": "Admin",
                "applications": [
                    {
                        "applicationID": "",
                        "application_name": "blank",
                        "application_namespace": "blank",
                        "application_desc": "Blank app without any microservices",
                        "microservices": [],
                    }
                ],
            }

            self.response = self.core.http_method.call(
                # url=url, json=_json, headers=headers, verify=verify
                url=url,
                json=test_json,
                headers=headers,
                verify=verify,
            )

            ic("bbbbbbbbbbbbbb")
            ic(self.response)

            self.response.status = HTTPStatus(self.response.status_code)

            ic("cccccccccccccccc")

            if self.response.status == HTTPStatus.OK:
                ic("dddddddddddd")
                if self.aux.show_msg_on_success:
                    logger.info(f"Success: '{self.aux.what_should_happen}'")
                ic("eeeeeeeeeeeeeeeeeee")
                response = self.response.json()
                if isinstance(response, str):
                    response = json.loads(response)

                ic("ffffffffffffffffffff")
                return response

        except requests.exceptions.RequestException as e:
            ic("oOOOOOOOOOOOOOOOOOOOOOOOO")
            ic(e)

            error_msg = f"exception: {e}: "

        error_msg += self._create_failure_msg()
        raise self.aux.exception(
            msg=error_msg,
            http_status=self.response.status if self.response else None,
            flops_identifier=self.aux.flops_identifier,
        )
