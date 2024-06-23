from learner_parts.main import start_cluster_aggregator_as_learner
from utils.arg_parsing import parse_args

if __name__ == "__main__":
    cluster_aggregator_context = parse_args()
    # handle_aggregator(cluster_aggregator_context)
    start_cluster_aggregator_as_learner(cluster_aggregator_context)
