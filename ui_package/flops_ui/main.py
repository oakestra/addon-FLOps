#!/usr/bin/env python3
import threading

from flops_ui.mqtt.main import handle_mqtt, notify_flops_manager
from flops_ui.oak_service_communication import handle_oak_service_communication
from flops_ui.utils.arg_parsing import parse_args


def main() -> None:
    parse_args()
    try:
        threading.Thread(target=handle_mqtt).start()
        handle_oak_service_communication()
    except Exception as e:
        notify_flops_manager(f"Something unexpected went wrong. '{e}'")


if __name__ == "__main__":
    main()
