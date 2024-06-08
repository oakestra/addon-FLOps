from mock_data_provider.data_loader import load_and_send_data_to_server
from mock_data_provider.utils.arg_parsing import parse_args


def main():
    parse_args()
    load_and_send_data_to_server()


if __name__ == "__main__":
    main()
