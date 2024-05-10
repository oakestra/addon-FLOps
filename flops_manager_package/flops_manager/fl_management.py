from flops_manager.classes.apps.observatory.management import get_observatory
from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.observatory.project_observer import FLOpsProjectObserver
from flops_manager.classes.services.observatory.tracking_server import TrackingServer
from flops_manager.classes.services.project.aggregator.main import FLAggregator
from flops_manager.classes.services.project.learners import FLLearners
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger


def handle_fl_operations(flops_project: FLOpsProject) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    observatory = get_observatory(flops_project.customer_id)
    tracking_server = TrackingServer(parent_app=observatory)
    project_observer = retrieve_from_db_by_project_id(
        FLOpsProjectObserver, flops_project.flops_project_id
    )

    fl_aggregator = FLAggregator(
        parent_app=flops_project,
        project_observer_ip=project_observer.ip,
        tracking_server_url=tracking_server.get_url(),
    )
    FLLearners(parent_app=flops_project, fl_aggregator_ip=fl_aggregator.ip)

    # TODO
