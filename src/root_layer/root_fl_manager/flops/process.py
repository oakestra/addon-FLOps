from utils.classes.base import FlOpsBaseClass


class FlOpsProcess(FlOpsBaseClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False
    flops_process_id: str = ""

    def model_post_init(self, _):
        if not self.flops_process_id:
            flops_db_id = self._add_to_db()
            self.flops_process_id = str(flops_db_id)
            self._replace_in_db(flops_db_id)

    def get_shortened_id(self) -> str:
        return self.flops_process_id[:6]
