from flops_manager.image_management.common import get_flops_image_prefix


def get_trained_model_image_name(
    customer_id: str,
    run_id: str,
) -> str:
    return "".join(
        (
            get_flops_image_prefix(),
            "/",
            customer_id.lower(),
            "/",
            "trained_model",
            ":",
            run_id,
        )
    )
