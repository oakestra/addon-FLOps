from utils.classes.simple import CustomEnum


class Topics(CustomEnum):
    IMAGE_BUILDER_SUCCESS = "root_fl_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "root_fl_manager/image_builder/failed"
    FL_UI_FAILED = "root_fl_manager/fl_ui/failed"
