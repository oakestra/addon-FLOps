#!/usr/bin/env python3

import threading

from flops_manager.api.main import handle_api
from flops_manager.database.main import FLOpsDB
from flops_manager.mqtt.main import handle_mqtt
from flops_manager.utils.certificate_management import handle_ca_and_certificates


def main():
    handle_ca_and_certificates()
    FLOpsDB()
    threading.Thread(target=handle_api).start()
    handle_mqtt()


if __name__ == "__main__":
    main()
