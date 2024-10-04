import http
from typing import List

from flops_manager.classes.apps.app_base import FLOpsApp
from flops_manager.database.common import add_to_db, replace_in_db
from flops_manager.ml_repo_management import get_latest_commit_hash
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.exceptions.types import FlOpsExceptionTypes
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from flops_manager.utils.types import Application, PostTrainingSteps
from flops_utils.types import FLOpsMode, MLModelFlavor, PlatformSupport
from pydantic import AliasChoices, BaseModel, Field

# TODO/Future Work: Add additional Pydantic checking:
# e.g.: training_rounds > 1
#       min_..._clients > 1, etc.


# NOTE: Using BaseModel instead of NamedTuple here allows for nicer serialized data in the DB.
class _TrainingConfiguration(BaseModel):
    mode: FLOpsMode = Field(default=FLOpsMode.CLASSIC)
    data_tags: List[str] = Field(
        default_factory=list,
        description=" ".join(
            (
                "Data tags are used to select and find data that is stored in the ML-Data-Servers",
                "and that should be used for this FLOps project.",
            )
        ),
    )
    training_cycles: int = Field(
        default=1,
        description="""
        (Only applicable for the 'hierarchical' mode.)
        The number of training & evaluation rounds performed between
        the root aggregator (RAg) and cluster aggregators (CAg).
        Example: training_cycles = 2, training_rounds = 3:
        - The first training cycle starts:
            The learners train and share their results with their CAg.
            After 3 such training rounds the aggregated cluster results are send to the RAg.
        - The second training cycle starts:
            The learners train and share their results again with their CAg.
            After 3 training rounds the aggregated cluster results are again send to the RAg.
        - The whole training period has come to an end.
        """,
    )
    training_rounds: int = Field(
        default=3,
        description="The number of training & evaluations rounds performed on a learner.",
    )

    # NOTE: In the hierarchical mode these values are per cluster not in total.
    # I.e. 2 'min_learners' -> 2 per cluster.
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1


class _ResourceConstraints(BaseModel):
    # TODO: Fine-tune these values. + incorporate them in the final Project component SLAs.
    memory: int = 100
    vcpus: int = 1
    storage: int = 0


class FLOpsProject(FLOpsApp):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    namespace = "proj"

    customer_id: str = Field(
        default="Admin",
        alias=AliasChoices("customer_id", "customerID"),  # type: ignore
    )
    verbose: bool = False
    use_devel_base_images: bool = False
    supported_platforms: List[PlatformSupport] = Field(
        default_factory=lambda: [PlatformSupport.LINUX_AMD64]
    )

    ml_model_flavor: MLModelFlavor

    training_configuration: _TrainingConfiguration = _TrainingConfiguration()
    resource_constraints: _ResourceConstraints = _ResourceConstraints()
    post_training_steps: List[PostTrainingSteps] = Field(default_factory=list)

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

        # NOTE: This check can/should be refactored via a proper Pydantic approach.
        if self.use_devel_base_images and self.supported_platforms != [PlatformSupport.LINUX_AMD64]:
            raise FLOpsManagerException(
                flops_exception_type=FlOpsExceptionTypes.INITIAL_PROJECT_SLA_MISCONFIGURATION,
                http_status=http.HTTPStatus.BAD_REQUEST,
                text="Development Base Images can only be used for Linux/amd64.",
            )

        self.ml_repo_latest_commit_hash = get_latest_commit_hash(self.ml_repo_url)
        flops_db_id = add_to_db(self)
        self._configure_sla_components(str(flops_db_id))
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
