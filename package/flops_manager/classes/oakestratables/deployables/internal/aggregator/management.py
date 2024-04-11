from flops_manager.classes.oakestratables.deployables.internal.aggregator.main import FLAggregator

# from flops.classes.project import FlOpsProject
# from flops.classes.ui import FLUserInterface
from flops_manager.utils.common import notify_ui

# from flops_manager.utils.logging import logger


# def init_aggregator(flops_project: FlOpsProject, ui: FLUserInterface) -> None:
def init_aggregator(flops_project, ui) -> None:
    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="Preparing new FL Aggregator.",
        )

    FLAggregator(flops_project=flops_project, ui=ui)

    if flops_project.verbose:
        notify_ui(
            flops_project_id=flops_project.flops_project_id,
            msg="New Aggregator service created & deployed",
        )


# def handle_builder_success(builder_success_msg: dict) -> None:
#     logger.debug(builder_success_msg)
#     flops_project_id = builder_success_msg["flops_project_id"]
#     FLClientEnvImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
#     main_flops.handle_fl_operations(
#         flops_project=FlOpsProject.retrieve_from_db(flops_project_id=flops_project_id),
#         fl_client_image=builder_success_msg["image_name_with_tag"],
#     )


# def handle_builder_failed(builder_failed_msg: dict) -> None:
#     logger.debug(builder_failed_msg)
#     flops_project_id = builder_failed_msg["flops_project_id"]
#     FLClientEnvImageBuilder.retrieve_from_db(flops_project_id=flops_project_id).undeploy()
#     msg = "Builder failed. Terminating this FLOps."
#     logger.critical(msg)
#     notify_ui(flops_project_id=flops_project_id, msg=msg)
