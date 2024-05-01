from flops_manager.classes.oak.project_based import FlOpsOakestraProjectBasedClass
from flops_manager.ml_repo_management import MLRepoInfo, get_latest_commit_hash
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from pydantic import AliasChoices, BaseModel, Field

# TODO/Future Work: Add additional Pydantic checking:
# e.g.: training_rounds > 1
#       min_..._clients > 1, etc.


# Note: Using BaseModel instead of NamedTuple here allows for nicer serialized data in the DB.
class _TrainingConfiguration(BaseModel):
    training_rounds: int = 3
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1


class _ResourceContraints(BaseModel):
    # TODO: Fine-tune these values. + incorporate them in the final Project component SLAs.
    memory: int = 100
    vcpus: int = 1
    storage: int = 0


class FlOpsProject(FlOpsOakestraProjectBasedClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))
    verbose: bool = False

    # Note: The ml_repo_url is only used as an input param and then discarded.
    ml_repo_url: str = Field(repr=False, exclude=True)
    ml_repo_info: MLRepoInfo = Field(None, init=False)

    training_configuration: _TrainingConfiguration = _TrainingConfiguration()
    resource_constraints: _ResourceContraints = _ResourceContraints()

    flops_project_id: str = Field(
        "",
        init=False,
        description="Is the same as its application ID in Oakestra",
    )

    namespace = "flopsproject"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.ml_repo_info = MLRepoInfo(url=self.ml_repo_url)
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
                    app_name=f"flopsproject{self.get_shortened_id(str(flops_db_id))}",
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="Internal application for managing FLOps services"),
        )

    def get_shortened_id(self, specific_id: str = "") -> str:
        return (specific_id or self.flops_project_id)[:6]
