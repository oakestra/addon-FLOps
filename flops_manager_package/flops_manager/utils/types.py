import enum


class PostTrainingSteps(str, enum.Enum):
    BUILD_IMAGE_FOR_TRAINED_MODEL = "build_image_for_trained_model"
    DEPLOY_TRAINED_MODEL_IMAGE = "deploy_trained_model_image"


SLA = dict
AppSLA = SLA

Application = dict
Service = dict

Id = str
ServiceId = Id
ApplicationId = Id
