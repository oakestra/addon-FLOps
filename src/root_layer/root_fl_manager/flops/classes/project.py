from flops.classes.abstract.oakestratable import FlOpsOakestraClass
from pydantic import Field
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames


class FlOpsProject(FlOpsOakestraClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False

    flops_project_id: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return
        flops_db_id = self._add_to_db()
        self._configure_sla_components(flops_db_id)
        self.create(standalone=True)
        self.flops_project_id = self.app_id
        self._replace_in_db(flops_db_id)

    def _configure_sla_components(self, flops_db_id: str) -> None:
        app_name = f"fl{self.get_shortened_id(str(flops_db_id))}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(app_name=app_name, app_namespace="flops"),
            ),
            details=SlaDetails(app_desc="Internal application for managing FLOps services"),
        )

    def get_shortened_id(self, specific_id: str = "") -> str:
        return (specific_id or self.flops_project_id)[:6]
