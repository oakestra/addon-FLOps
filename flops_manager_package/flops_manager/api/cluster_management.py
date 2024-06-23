from typing import List

from flops_manager.api.request_management.custom_requests import (
    CustomRequest,
    RequestAuxiliaries,
    RequestCore,
)
from flops_manager.api.utils.consts import SYSTEM_MANAGER_URL
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes


def get_active_clusters_from_orchestrator() -> List[dict]:
    active_clusters = CustomRequest(
        core=RequestCore(
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/clusters/active",
        ),
        aux=RequestAuxiliaries(
            what_should_happen="Get active clusters",
            flops_exception_type=FlOpsExceptionTypes.ACTIVE_CLUSTERS,
            show_msg_on_success=True,
        ),
    ).execute()
    return active_clusters
