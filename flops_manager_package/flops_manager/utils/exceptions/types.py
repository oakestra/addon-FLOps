from flops_utils.types import CustomEnum


class FlOpsExceptionTypes(CustomEnum):
    UNSPECIFIED = "Unspecified FLOps Manager Error"
    IMAGE_BUILDER = "Image Builder"
    FL_AGGREGATOR = "FL Aggregator"
    MQTT = "MQTT"
    IMAGE_REGISTRY = "Image Registry"
    LOGIN = "Login"
    APP_CREATE = "Application Creation"
    APP_DELETE = "Application Deletion"
    APP_FETCH = "Fetching Application from Oakestra"
    INTERNAL_PROJECT_SERVICE_APPEND = "Appending internal FLOps service to FLOps Project"
    SERVICE_DEPLOYMENT = "Deploying Service"
    SERVICE_UNDEPLOYMENT = "Undeploying Service"
    ACTIVE_CLUSTERS = "Active Clusters"
