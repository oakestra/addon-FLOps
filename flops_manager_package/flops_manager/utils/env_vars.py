from flops_utils.env_vars import get_env_var

SYSTEM_MANAGER_IP = get_env_var("SYSTEM_MANAGER_IP")
SYSTEM_MANAGER_PORT = get_env_var("SYSTEM_MANAGER_PORT", "1000")

FLOPS_MANAGER_IP = get_env_var("FLOPS_MANAGER_IP")
FLOPS_MANAGER_PORT = get_env_var("FLOPS_MANAGER_PORT", "5072")
FLOPS_DB_PORT = get_env_var("FLOPS_DB_PORT", "10027")

FLOPS_MQTT_BROKER_IP = get_env_var("FLOPS_MQTT_BROKER_IP")
FLOPS_MQTT_BROKER_PORT = get_env_var("FLOPS_MQTT_BROKER_PORT", "9027")

FLOPS_IMAGE_REGISTRY_IP = get_env_var("FLOPS_IMAGE_REGISTRY_IP")
ARTIFACT_STORE_IP = get_env_var("ARTIFACT_STORE_IP")
BACKEND_STORE_IP = get_env_var("BACKEND_STORE_IP")

ML_DATA_SERVER_PORT = 11027

TRAINED_MODEL_PORT = 8080
