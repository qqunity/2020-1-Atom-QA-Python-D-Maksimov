import pytest

from linux_settings.remote_control.remote_connection import SSH


@pytest.fixture(scope='session')
def ssh_connector():
    with SSH(hostname='192.168.1.15', username='centos', password='centos', port=2002) as ssh:
        yield ssh
