from typing import Optional

from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.classes.oakestratables.deployables.image_registry.main import FLOpsImageRegistry
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_manager.utils.types import Application

_flops_image_builder = None

# TODO methode aufteilen - parsing is ready,
# + fall pruefen wenn die app noch nicht da ist - da muss ich die custom requests minimal anpassen + new flag to allow non 200 responses
# sobald das fertig ist kann ich endlich pruefen ob die arbeit worth war und client klappt!!


def _fetch_registry_app() -> Application:
    return CustomRequest(
        core=RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="".join(
                (
                    "/api/application/",
                    FLOpsImageRegistry.namespace,
                    "/",
                    FLOpsImageRegistry.namespace,
                )
            ),
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get current flops image registry application",
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        ),
    ).execute()


def _check_if_registry_already_exists_in_oak() -> Optional[FLOpsImageRegistry]:
    app = _fetch_registry_app()
    if not app:
        return None

    service = CustomRequest(
        core=RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{app['microservices'][0]}",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get current flops image registry service",
            flops_exception_type=FlOpsExceptionTypes.IMAGE_REGISTRY,
        ),
    ).execute()
    service["gets_loaded_from_db"] = True
    return FLOpsImageRegistry.model_validate(service)


def init_or_fetch_flops_image_registry() -> FLOpsImageRegistry:
    global _flops_image_builder
    res = _check_if_registry_already_exists_in_oak()
    _flops_image_builder = res or FLOpsImageRegistry()
    return _flops_image_builder


def get_flops_image_registry() -> FLOpsImageRegistry:
    if not _flops_image_builder:
        return init_or_fetch_flops_image_registry()
    return _flops_image_builder
