from dataclasses import dataclass

from context.main import Context


@dataclass
class ContextTrainedModel(Context):
    run_id: str
