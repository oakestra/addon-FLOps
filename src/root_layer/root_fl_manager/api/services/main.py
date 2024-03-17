from typing import Dict

import requests
from api.utils import create_system_manager_api_query
from utils.logging import logger


def update_service_image(service: Dict, existing_image_name: str) -> None:
    service["image"] = existing_image_name
    service_id = service["microserviceID"]
    logger.debug("E#" * 10)

    url, headers, _ = create_system_manager_api_query(f"/api/services/{service_id}")
    logger.debug("F#" * 10)

    # response = requests.put(url, json=service)
    logger.debug(url)
    logger.debug(headers)
    logger.debug("G#" * 10)
    response = requests.get(url, headers=headers)

    logger.debug("H#" * 10)
    logger.debug(response)
    logger.debug(response.json())
    logger.debug("h-" * 10)
