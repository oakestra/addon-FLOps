import threading

from api.main import handle_api
from mqtt.main import handle_mqtt
from utils.certificate_management import handle_ca_and_certificates


def main():
    handle_ca_and_certificates()
    # Note: This RESTful Flask API has been kept for now in case It will get useful again in the future (instead of figuring out how to set it up from scratch again)
    # It needs to be started concurrently otherwise it will block and MQTT will not get started.
    # I.e. the Root FL Manager provides both - a RESTful API and a MQTT client.
    threading.Thread(target=handle_api).start()
    handle_mqtt()


if __name__ == "__main__":
    main()
