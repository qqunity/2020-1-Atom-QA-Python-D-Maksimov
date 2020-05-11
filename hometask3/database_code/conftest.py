import pytest

from database_code.mysql_client.client import MySQLConnection


@pytest.fixture(scope='session')
def mysql_client():
    return MySQLConnection('root', 'pass', 'nginx_logs')
