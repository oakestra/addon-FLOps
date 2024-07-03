from __future__ import annotations

from typing import TYPE_CHECKING

from flops_manager.api.cluster_management import get_active_clusters_from_orchestrator
from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.observatory.tracking_server.management import (
    get_tracking_server,
)
from flops_manager.classes.services.project.aggregators.classic_aggregator import (
    ClassicFLAggregator,
)
from flops_manager.classes.services.project.aggregators.cluster_aggregator import (
    ClusterFLAggregator,
)
from flops_manager.classes.services.project.aggregators.root_aggregator import RootFLAggregator
from flops_manager.classes.services.project.learners.main import FLLearners
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger
from flops_utils.types import FLOpsMode

if TYPE_CHECKING:
    from flops_manager.classes.apps.project import FLOpsProject


def handle_fl_training_processes(flops_project: FLOpsProject) -> None:
    msg = "Start handling FL training processes"
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    tracking_server = get_tracking_server(flops_project.customer_id)
    project_observer = retrieve_from_db_by_project_id(
        FLOpsProjectObserver, flops_project.flops_project_id
    )

    if flops_project.training_configuration.mode == FLOpsMode.CLASSIC:
        fl_aggregator = ClassicFLAggregator(
            parent_app=flops_project,
            project_observer_ip=project_observer.ip,  # type: ignore
            tracking_server_url=tracking_server.get_url(),
        )
        FLLearners(
            parent_app=flops_project,
            fl_aggregator_ip=fl_aggregator.ip,
            project_observer_ip=project_observer.ip,  # type: ignore
            tracking_server_url=tracking_server.get_url(),
        )
    else:

        # API request to OAK DB to figure out num of active clusters
        # GET /api/clusters/active
        active_clusters = get_active_clusters_from_orchestrator()

        # TODO Delete
        dummy_cluster = active_clusters[0].copy()
        dummy_cluster["cluster_name"] = "dummy"
        dummy_cluster["_id"] = "111111111111111111111111"
        active_clusters.append(dummy_cluster)

        root_fl_aggregator = RootFLAggregator(
            parent_app=flops_project,
            project_observer_ip=project_observer.ip,  # type: ignore
            tracking_server_url=tracking_server.get_url(),
            number_of_cluster_aggregators=len(active_clusters),
        )

        for cluster in active_clusters:
            cluster_name = cluster["cluster_name"]
            cluster_id = cluster["_id"]

            cluster_fl_aggregator = ClusterFLAggregator(
                parent_app=flops_project,
                root_fl_aggregator_ip=root_fl_aggregator.ip,
                project_observer_ip=project_observer.ip,  # type: ignore
                tracking_server_url=tracking_server.get_url(),
                cluster_name=cluster_name,
                cluster_id=cluster_id,
            )
            FLLearners(
                parent_app=flops_project,
                fl_aggregator_ip=cluster_fl_aggregator.ip,
                project_observer_ip=project_observer.ip,  # type: ignore
                tracking_server_url=tracking_server.get_url(),
                cluster_name=cluster_name,
                cluster_id=cluster_id,
            )
