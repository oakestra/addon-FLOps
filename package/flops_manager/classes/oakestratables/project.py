from flops_manager.classes.oakestratables.project_based import FlOpsOakestraProjectBasedClass
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from pydantic import Field


class FlOpsProject(FlOpsOakestraProjectBasedClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False

    flops_project_id: str = Field(
        "",
        init=False,
        description="Is the same as its application ID in Oakestra",
    )

    namespace = "flopspro"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        flops_db_id = self._add_to_db()
        self._configure_sla_components(flops_db_id)
        created_app = self.create()
        self._set_properties_based_on_created_result(created_app)
        self.flops_project_id = created_app["applicationID"]
        self._replace_in_db(flops_db_id)

    def _configure_sla_components(self, flops_db_id: str) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=f"pr{self.get_shortened_id(str(flops_db_id))}",
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="Internal application for managing FLOps services"),
        )

    def get_shortened_id(self, specific_id: str = "") -> str:
        return (specific_id or self.flops_project_id)[:6]
