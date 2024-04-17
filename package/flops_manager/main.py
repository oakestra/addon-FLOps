#!/usr/bin/env python3

import threading

from flops_manager.api.main import handle_api
from flops_manager.database.main import FLOpsDB
from flops_manager.mqtt.listener import init_mqtt_listener


def main():
    FLOpsDB()
    threading.Thread(target=handle_api).start()
    init_mqtt_listener()


if __name__ == "__main__":
    main()
