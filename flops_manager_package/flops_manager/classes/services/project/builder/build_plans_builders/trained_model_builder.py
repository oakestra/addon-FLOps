from flops_manager.classes.services.project.builder.base_builder import FLOpsBaseImageBuilder
from pydantic import Field


class TrainedModelImageBuilder(FLOpsBaseImageBuilder):
    tracking_server_uri: str = Field(examples=["http://192.168.178.44:7027"])
    run_id: str = Field(description="The MLflow run-id of the trained model")

    def _prepare_cmd(self) -> str:
        cmd = super()._prepare_cmd()
        cmd += (
            f" trained_model {self.parent_app.customer_id} {self.tracking_server_uri} {self.run_id}"
        )
        return cmd
