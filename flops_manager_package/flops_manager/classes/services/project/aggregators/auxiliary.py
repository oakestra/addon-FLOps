from flops_manager.classes.services.project.aggregators.classic_aggregator import (
    ClassicFLAggregator,
)
from flops_manager.classes.services.project.aggregators.cluster_aggregator import (
    ClusterFLAggregator,
)
from flops_manager.classes.services.project.aggregators.root_aggregator import RootFLAggregator
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_utils.types import AggregatorType


def _get_matching_aggregator_class(
    aggregator_type: AggregatorType,
) -> type[ClassicFLAggregator] | type[RootFLAggregator] | type[ClusterFLAggregator]:
    match aggregator_type:
        case AggregatorType.CLASSIC_AGGREGATOR:
            return ClassicFLAggregator
        case AggregatorType.ROOT_AGGREGATOR:
            return RootFLAggregator
        case AggregatorType.CLUSTER_AGGREGATOR:
            return ClusterFLAggregator


def get_matching_aggregator_class_based_on_project_id(flops_project_id: str):
    if retrieve_from_db_by_project_id(ClassicFLAggregator, flops_project_id):
        return ClassicFLAggregator

    if retrieve_from_db_by_project_id(RootFLAggregator, flops_project_id):
        return RootFLAggregator

    if retrieve_from_db_by_project_id(ClusterFLAggregator, flops_project_id):
        return ClusterFLAggregator


def handle_aggregator_success(aggregator_success_msg: dict) -> None:
    aggregator_type = AggregatorType(aggregator_success_msg["aggregator_type"])
    _get_matching_aggregator_class(aggregator_type).handle_aggregator_success(
        aggregator_success_msg
    )


def handle_aggregator_failed(aggregator_failed_msg: dict) -> None:
    aggregator_type = AggregatorType(aggregator_failed_msg["aggregator_type"])
    _get_matching_aggregator_class(aggregator_type).handle_aggregator_failed(aggregator_failed_msg)
