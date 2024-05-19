from mock_data_provider.data_loader import load_data
from mock_data_provider.data_sender import send_data_to_data_manager


def main():
    dataset_partition = load_data()
    send_data_to_data_manager(dataset_partition)


if __name__ == "__main__":
    main()
