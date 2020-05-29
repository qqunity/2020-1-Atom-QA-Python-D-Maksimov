import pytest

from api.client import ApiClient
from conftest import ApiSettings
from database_code.db_interaction.interaction import DbInteraction
from tests.utils import Logger


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config_api, get_database_interaction):
        self.config: ApiSettings = config_api
        self.api_client: ApiClient = ApiClient(config_api)
        self.db_interaction: DbInteraction = get_database_interaction
        self.logger: Logger = Logger(self.config.log_writer_path)
