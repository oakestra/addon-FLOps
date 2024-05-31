from aggregator_management import handle_aggregator
from utils.arg_parsing import parse_args

if __name__ == "__main__":
    aggregator_context = parse_args()
    handle_aggregator(aggregator_context)
