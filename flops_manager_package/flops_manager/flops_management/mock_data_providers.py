from flops_manager.classes.apps.helper import FLOpsHelperApp
from flops_manager.classes.services.helper.mock_data_provider import MockDataProvider


def handle_new_mock_data_provider(request_data: dict, bearer_token: str) -> None:
    request_data["parent_app"] = FLOpsHelperApp.get_app(customer_id=request_data["customerID"])
    request_data["bearer_token"] = bearer_token
    MockDataProvider.model_validate(request_data)
