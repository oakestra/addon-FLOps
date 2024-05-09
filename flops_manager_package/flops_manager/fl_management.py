from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.deployables.project_services.aggregator.main import FLAggregator
from flops_manager.classes.deployables.project_services.learners import FLLearners
from flops_manager.classes.services.project_observer import FLOpsProjectObserver
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.mqtt.sender import notify_project_observer
from flops_utils.logging import colorful_logger as logger


def handle_fl_operations(flops_project: FLOpsProject) -> None:
    msg = "Start handling FL processes"
    logger.info(msg)
    notify_project_observer(flops_project_id=flops_project.flops_project_id, msg=msg)

    project_observer = retrieve_from_db_by_project_id(
        FLOpsProjectObserver, flops_project.flops_project_id
    )

    fl_aggregator = FLAggregator(
        flops_project=flops_project, project_observer_ip=project_observer.ip
    )
    FLLearners(flops_project=flops_project, fl_aggregator=fl_aggregator)

    # TODO
