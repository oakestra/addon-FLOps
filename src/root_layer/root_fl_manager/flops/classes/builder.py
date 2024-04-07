# from flops.classes.abstract.deyployable import FlOpsDeployableClass


# class FLClientEnvImageBuilder(FlOpsDeployableClass):
class FLClientEnvImageBuilder:
    pass
    # def __init__(self, flops_process: FlOpsProcess, ml_repo: MlRepo, fl_ui: FLUserInterface):

    # def _prepare_sla(self, flops_process: FlOpsProcess) -> AppSLA:
    #     return generate_builder_sla(ml_repo, flops_process, fl_ui)


# def handle_builder_success(builder_success_msg: dict) -> None:
#     logger.debug(builder_success_msg)
#     image_name_with_tag = builder_success_msg["image_name_with_tag"]
#     flops_process_id = builder_success_msg["flops_process_id"]

#     undeploy_builder_app(flops_process_id)
#     flops.main.handle_fl_operations(FlOpsProcess(flops_process_id), image_name_with_tag)


# def handle_builder_failed(builder_failed_msg: dict) -> None:
#     logger.debug(builder_failed_msg)
#     flops_process_id = builder_failed_msg["flops_process_id"]
#     undeploy_builder_app(flops_process_id)
#     msg = "Builder failed. Terminating this FLOps."
#     logger.critical(msg)
#     ui_notifier.notify_ui(msg, FlOpsProcess(flops_process_id))
