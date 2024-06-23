from __future__ import annotations

from typing import TYPE_CHECKING

from flops_manager.classes.apps.project import FLOPsMode
from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.observatory.tracking_server.management import (
    get_tracking_server,
)
from flops_manager.classes.services.project.aggregators.main import FLAggregator
from flops_manager.classes.services.project.aggregators.root_aggregator import RootFLAggregator
from flops_manager.classes.services.project.learners import FLLearners
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger
from icecream import ic

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

    if flops_project.training_configuration.mode == FLOPsMode.CLASSIC:
        fl_aggregator = FLAggregator(
            parent_app=flops_project,
            project_observer_ip=project_observer.ip,
            tracking_server_url=tracking_server.get_url(),
        )
        FLLearners(
            parent_app=flops_project,
            fl_aggregator_ip=fl_aggregator.ip,
            project_observer_ip=project_observer.ip,
            tracking_server_url=tracking_server.get_url(),
        )
    else:

        # API request to OAK DB to figure out num of active clusters
        # GET /api/clusters/active
        number_of_active_clusters = 1  # TODO

        root_fl_aggregator = RootFLAggregator(
            parent_app=flops_project,
            project_observer_ip=project_observer.ip,
            tracking_server_url=tracking_server.get_url(),
            number_of_active_clusters=number_of_active_clusters,
        )
