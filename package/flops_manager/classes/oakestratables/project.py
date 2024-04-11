from flops_manager.classes.oakestratables.base import FlOpsOakestraBaseClass
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from pydantic import Field


class FlOpsProject(FlOpsOakestraBaseClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False

    flops_project_id: str = Field(
        "",
        init=False,
        description="Is the same as its application ID in Oakestra",
    )
    project_app_name: str = Field("", init=False)

    namespace = "flopspro"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        flops_db_id = self._add_to_db()
        self.project_app_name = f"pr{self.get_shortened_id(str(flops_db_id))}"
        self._configure_sla_components(flops_db_id)
        self.create()
        self._replace_in_db(flops_db_id)

    def _configure_sla_components(self, flops_db_id: str) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.project_app_name,
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="Internal application for managing FLOps services"),
        )

    def get_shortened_id(self, specific_id: str = "") -> str:
        return (specific_id or self.flops_project_id)[:6]
