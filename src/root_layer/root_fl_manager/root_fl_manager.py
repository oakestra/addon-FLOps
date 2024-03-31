#!/usr/bin/env python3

import threading

from api.main import handle_api
from mqtt.main import handle_mqtt
from utils.certificate_management import handle_ca_and_certificates


def main():
    handle_ca_and_certificates()
    threading.Thread(target=handle_api).start()
    handle_mqtt()


if __name__ == "__main__":
    main()
