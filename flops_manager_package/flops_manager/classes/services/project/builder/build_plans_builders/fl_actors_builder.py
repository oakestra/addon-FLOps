from flops_manager.classes.services.project.builder.base_builder import FLOpsBaseImageBuilder


class FLActorsImageBuilder(FLOpsBaseImageBuilder):
    def _prepare_cmd(self) -> str:
        cmd = super()._prepare_cmd()
        cmd += f" fl_actors {self.parent_app.ml_repo_url} {self.parent_app.ml_model_flavor}"
        if self.parent_app.use_devel_base_images:
            cmd += " --use-devel-base-images"
        return cmd
