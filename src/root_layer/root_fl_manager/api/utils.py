import json
from http import HTTPStatus
from typing import NamedTuple, Optional, Tuple

import requests
from api.common import HttpMethod
from api.login import get_login_token
from utils.logging import logger


class ApiQueryComponents(NamedTuple):
    url: str
    headers: dict
    data: dict = None


def _prepare_api_query_components(
    base_url: str,
    api_endpoint: str = None,
    custom_headers: dict = None,
    data: dict = None,
    query_params: str = None,
    is_oakestra_api: bool = True,
) -> ApiQueryComponents:
    url = base_url
    if api_endpoint is not None:
        url = f"{base_url}{api_endpoint}"
    if query_params is not None:
        url += f"?{query_params}"

    if custom_headers:
        headers = custom_headers
    else:
        headers = {"Authorization": f"Bearer {get_login_token()}"} if is_oakestra_api else {}

    if data and not custom_headers:
        headers["Content-Type"] = "application/json"
    return ApiQueryComponents(url, headers, data)


def _create_failure_msg(
    what_should_happen: str,
    http_method: HttpMethod,
    url: str,
    response_status: HTTPStatus = None,
) -> str:
    return (
        " ".join(
            (
                what_should_happen,
                "request failed with",
                str(response_status),
                f"for '{http_method}' '{url}",
            )
        ),
    )


def handle_request(
    base_url: str,
    what_should_happen: str,
    http_method: HttpMethod = HttpMethod.GET,
    api_endpoint: str = None,
    headers: dict = None,
    data: dict = None,
    show_msg_on_success: bool = False,
    special_msg_on_fail: str = None,
    query_params: str = None,
    is_oakestra_api: bool = True,
) -> Tuple[HTTPStatus, Optional[dict]]:

    url, headers, data = _prepare_api_query_components(
        base_url,
        api_endpoint,
        headers,
        data,
        query_params,
        is_oakestra_api,
    )
    args = {
        "url": url,
        "verify": False,
        **({"headers": headers} if headers else {}),
        **({"json": data} if data else {}),
    }

    try:
        response = http_method.call(**args)
        response_status = HTTPStatus(response.status_code)
        if response_status == HTTPStatus.OK:
            if show_msg_on_success:
                logger.info(f"Success: '{what_should_happen}'")
            response = response.json()
            if isinstance(response, str):
                response = json.loads(response)
            return response_status, response
        else:
            logger.error(f"FAILED: '{special_msg_on_fail or what_should_happen}'!")
            logger.error(_create_failure_msg(what_should_happen, http_method, url, response_status))
            logger.error("response:", response)
            return response_status, None
    except requests.exceptions.RequestException as e:
        logger.error(_create_failure_msg(what_should_happen, http_method, url))
        logger.error(e)
        return HTTPStatus.INTERNAL_SERVER_ERROR, None
