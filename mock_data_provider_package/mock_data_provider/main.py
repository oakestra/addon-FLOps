from mock_data_provider.data_loader import load_data
from mock_data_provider.data_sender import send_data_to_ml_data_server
from mock_data_provider.utils.arg_parsing import parse_args


def main():
    parse_args()
    dataset_partition = load_data()
    send_data_to_ml_data_server(dataset_partition)


if __name__ == "__main__":
    main()
