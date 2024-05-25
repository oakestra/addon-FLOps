from typing import List

from flops_manager.classes.apps.app_base import FLOpsApp
from flops_manager.database.common import add_to_db, replace_in_db
from flops_manager.ml_repo_management import get_latest_commit_hash
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from flops_manager.utils.types import Application
from flops_utils.types import MLModelFlavor
from pydantic import AliasChoices, BaseModel, Field

# TODO/Future Work: Add additional Pydantic checking:
# e.g.: training_rounds > 1
#       min_..._clients > 1, etc.


# Note: Using BaseModel instead of NamedTuple here allows for nicer serialized data in the DB.
class _TrainingConfiguration(BaseModel):
    data_tags: List[str] = Field(
        default_factory=list,
        description=" ".join(
            (
                "Data tags are used to select and find data that is stored in the ML-Data-Servers",
                "and that should be used for this FLOps project.",
            )
        ),
    )
    training_rounds: int = 3
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1


class _ResourceContraints(BaseModel):
    # TODO: Fine-tune these values. + incorporate them in the final Project component SLAs.
    memory: int = 100
    vcpus: int = 1
    storage: int = 0


class FLOpsProject(FLOpsApp):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    namespace = "proj"

    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))
    verbose: bool = False
    use_devel_base_images: bool = False
    ml_model_flavor: MLModelFlavor

    training_configuration: _TrainingConfiguration = _TrainingConfiguration()
    resource_constraints: _ResourceContraints = _ResourceContraints()

    ml_repo_url: str
    ml_repo_latest_commit_hash: str = Field("", init=False)

    flops_project_id: str = Field(
        "",
        init=False,
        description="Is the same as its application ID in the orchestrator",
    )

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.ml_repo_latest_commit_hash = get_latest_commit_hash(self.ml_repo_url)
        flops_db_id = add_to_db(self)
        self._configure_sla_components(flops_db_id)
        created_app = self._create_in_orchestrator()
        self._set_properties_based_on_created_result(created_app)
        replace_in_db(self, flops_db_id)

    def _configure_sla_components(self, flops_db_id: str) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=f"proj{get_shortened_unique_id(str(flops_db_id))}",
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="Internal application for managing FLOps services"),
        )

    def _set_properties_based_on_created_result(self, created_app: Application) -> None:
        self.flops_project_id = created_app["applicationID"]
        super()._set_properties_based_on_created_result(created_app)
