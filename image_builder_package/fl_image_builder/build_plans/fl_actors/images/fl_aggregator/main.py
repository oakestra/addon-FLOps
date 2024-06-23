from aggregator_management import handle_aggregator

# from learner_parts.main import start_cluster_aggregator_as_learner
from utils.aggregator_context import AggregatorType
from utils.arg_parsing import parse_args

if __name__ == "__main__":
    cluster_aggregator_context = parse_args()
    if cluster_aggregator_context.aggregator_type == AggregatorType.CLUSTER_AGGREGATOR:
        #        start_cluster_aggregator_as_learner(cluster_aggregator_context)
        pass
    else:
        handle_aggregator(cluster_aggregator_context)
