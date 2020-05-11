import random
import pytest

from sqlalchemy import desc
from database_code.models.models import LogInfo
from database_code.mysql_client.client import MySQLConnection
from database_code.tests.builder import MySQLBuilder
from faker import Faker

fake = Faker()


@pytest.mark.DB
class TestMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MySQLConnection = mysql_client
        self.builder = MySQLBuilder(mysql_client)
        self.log_path = '/media/qunity/Workspace/Python_projects/QA-python/hometask3/log_files'

    def test_create_record(self):
        self.builder.fill_database(self.log_path)
        some_log_info=f'{".".join(map(str, (random.randint(0, 255) for _ in range(4))))} - - [{random.randint(1, 30)}/{fake.month_name()}/{fake.date_time()}] "GET /downloads/product_1 HTTP/1.1" {random.randint(0, 600)} {random.randint(0, 125000)} "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)'
        some_log_info_id = self.builder.add_log_info(some_log_info).id
        query = self.mysql.session.query(LogInfo).order_by(desc(LogInfo.id)).limit(1).all()
        assert query[0].id == some_log_info_id
