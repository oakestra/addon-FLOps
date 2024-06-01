from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.project.builders.base_builder import FLOpsBaseImageBuilder
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.fl_management import handle_fl_training_processes


class FLActorsImageBuilder(FLOpsBaseImageBuilder):
    def _prepare_cmd(self) -> str:
        cmd = super()._prepare_cmd()
        cmd += f" fl_actors {self.parent_app.ml_repo_url} {self.parent_app.ml_model_flavor}"
        if self.parent_app.use_devel_base_images:
            cmd += " --use-devel-base-images"
        return cmd

    @classmethod
    def handle_builder_success(cls, builder_success_msg: dict) -> None:
        flops_project_id = super().handle_builder_success(builder_success_msg)
        handle_fl_training_processes(
            flops_project=retrieve_from_db_by_project_id(FLOpsProject, flops_project_id)
        )
