from datetime import datetime

import flops_manager.api.request_management.custom_requests as custom_requests
from flops_manager.api.request_management.custom_http import HttpMethods
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes

_login_token = ""
# NOTE: The token will become unusable after some time.
_last_login_time = None


def _login_and_set_token() -> str:
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/auth/login",
            data={"username": "Admin", "password": "Admin"},
            custom_headers={"accept": "application/json", "Content-Type": "application/json"},
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen="Login",
            flops_exception_type=FlOpsExceptionTypes.LOGIN,
        ),
    ).execute()

    global _login_token
    _login_token = response["token"]
    global _last_login_time
    _last_login_time = datetime.now()
    return _login_token


def get_login_token() -> str:
    if (
        _login_token == ""
        or _last_login_time is None
        or (datetime.now() - _last_login_time).total_seconds() > 10
    ):
        return _login_and_set_token()

    return _login_token
