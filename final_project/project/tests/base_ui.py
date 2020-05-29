import pytest

from database_code.db_interaction.interaction import DbInteraction
from tests.utils import Logger
from ui.pages.base import BaseActions
from ui.pages.login_page import LoginPage
from ui.pages.reg_page import RegPage
from vk_api_client.client import VkApiClient


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request, get_database_interaction, get_vk_api_client):
        self.driver = driver
        self.config = config
        self.login_page: LoginPage = request.getfixturevalue('login_page_object')
        self.db_interaction: DbInteraction = get_database_interaction
        self.vk_api_client: VkApiClient = get_vk_api_client
        self.logger: Logger = Logger(self.config['log_writer_path'])
