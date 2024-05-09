#!/usr/bin/env python3
import threading

from project_observer.mqtt.main import handle_mqtt, notify_flops_manager
from project_observer.oak_service_communication import handle_oak_service_communication
from project_observer.utils.arg_parsing import parse_args


def main() -> None:
    parse_args()
    try:
        threading.Thread(target=handle_mqtt).start()
        handle_oak_service_communication()
    except Exception as e:
        notify_flops_manager(f"Something unexpected went wrong. '{e}'")


if __name__ == "__main__":
    main()
