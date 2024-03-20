from http import HTTPStatus

import api.common
import api.utils

_login_token = ""


class LoginFailed(Exception):
    pass


def _login_and_set_token() -> str:
    data = {"username": "Admin", "password": "Admin"}
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        api_endpoint="/api/auth/login",
        headers=headers,
        data=data,
        what_should_happen="Login",
    )
    if status != HTTPStatus.OK:
        raise LoginFailed()

    global _login_token
    _login_token = json_data["token"]
    return _login_token


def get_login_token() -> str:
    if _login_token == "":
        return _login_and_set_token()
    return _login_token
