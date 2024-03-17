import os

import requests
from utils.types import CustomEnum


class HttpMethod(CustomEnum):
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"

    def call(cls, **kwargs) -> requests.Response:
        method_map = {
            cls.GET: requests.get,
            cls.POST: requests.post,
            cls.PATCH: requests.patch,
            cls.DELETE: requests.delete,
        }
        method = method_map.get(cls)

        if method:
            return method(**kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {cls.value}")


ROOT_FL_MANAGER_PORT = os.environ.get("ROOT_FL_MANAGER_PORT")

SYSTEM_MANAGER_IP = os.environ.get("SYSTEM_MANAGER_IP")
SYSTEM_MANAGER_PORT = os.environ.get("SYSTEM_MANAGER_PORT")
SYSTEM_MANAGER_URL = f"http://{SYSTEM_MANAGER_IP}:{SYSTEM_MANAGER_PORT}"

GITHUB_PREFIX = "https://github.com/"
