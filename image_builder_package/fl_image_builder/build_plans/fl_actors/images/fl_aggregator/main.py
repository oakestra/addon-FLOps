from aggregator_management import handle_aggregator
from flops_utils.types import AggregatorType
from learner_parts.main import start_cluster_aggregator_as_learner
from utils.arg_parsing import parse_args

if __name__ == "__main__":
    cluster_aggregator_context = parse_args()
    if cluster_aggregator_context.aggregator_type == AggregatorType.CLUSTER_AGGREGATOR:
        start_cluster_aggregator_as_learner(cluster_aggregator_context)
    else:
        handle_aggregator(cluster_aggregator_context)
