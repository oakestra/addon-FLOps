from .database import database_blp
from .mock_data_provider import mock_data_provider_blp
from .projects import projects_blp
from .tracking import tracking_blp

blueprints = [projects_blp, mock_data_provider_blp, tracking_blp, database_blp]
