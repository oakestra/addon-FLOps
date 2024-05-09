import os

from flops_manager.utils.types import CustomEnum

# TODO os.environ.get("FLOPS_MQTT_BROKER_URL")
# TODO need to figure out a way to provide
# non docker-compose member exclusive DNS name as IP.
# mqtt.main.ROOT_MQTT_BROKER_URL,
FLOPS_MQTT_BROKER_IP = "192.168.178.44"
FLOPS_MQTT_BROKER_PORT = os.environ.get("FLOPS_MQTT_BROKER_PORT")


class Topics(CustomEnum):
    PROJECT_OBSERVER_FAILED = "flops_manager/project_observer/failed"
    IMAGE_BUILDER_SUCCESS = "flops_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "flops_manager/image_builder/failed"
    AGGREGATOR_SUCCESS = "flops_manager/aggregator/success"
    AGGREGATOR_FAILED = "flops_manager/aggregator/failed"
