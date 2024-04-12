import os

from flops_manager.utils.types import CustomEnum

# TODO os.environ.get("FLOPS_MQTT_BROKER_URL")
FLOPS_MQTT_BROKER_URL = "192.168.178.44"
FLOPS_MQTT_BROKER_PORT = os.environ.get("FLOPS_MQTT_BROKER_PORT")


class Topics(CustomEnum):
    IMAGE_BUILDER_SUCCESS = "flops_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "flops_manager/image_builder/failed"
    FLOPS_UI_FAILED = "flops_manager/flops_ui/failed"
