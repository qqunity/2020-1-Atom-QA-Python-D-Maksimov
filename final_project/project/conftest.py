import pytest
import os
import subprocess
import logging
import allure

from dataclasses import dataclass
from ui.fixtures import *
from api.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--url', default='http://' + os.popen('./project/get_app_host').read().split('\n')[0] + ':8080/')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='83.0.4103.39')
    parser.addoption('--download_dir', default='./project/download_dir')
    parser.addoption('--username', default='test_q')
    parser.addoption('--password', default='test')
    parser.addoption('--log_path', default='./project/app_logs/log.txt')
    parser.addoption('--docker_compose_file_path',
                     default='./project/docker-compose.yml')
    parser.addoption('--selenoid', default=None)
    parser.addoption('--docker_url', default='http://project_app:8080/')
    parser.addoption('--log_writer_path', default='./project/app_logs/write_log_info')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    download_dir = request.config.getoption('--download_dir')
    selenoid_remote_ser = request.config.getoption('--selenoid')
    docker_url = request.config.getoption('--docker_url')
    log_writer_path = request.config.getoption('--log_writer_path')

    return {'browser': browser, 'version': version, 'url': url, 'download_dir': download_dir,
            'selenoid_remote_ser': selenoid_remote_ser, 'docker_url': docker_url, 'log_writer_path': log_writer_path}


@pytest.fixture(scope='function')
def run_app(request):
    log_path = request.config.getoption('--log_path')
    docker_compose_file = request.config.getoption('--docker_compose_file_path')
    if os.path.exists(log_path):
        os.remove(log_path)
    os.system(f'touch {log_path}')
    app = subprocess.run(["docker-compose", "--file", docker_compose_file, "up", "-d"], stdout=subprocess.PIPE,
                         text=True)
    app_healthy = False
    while not app_healthy:
        with open(log_path, 'r') as log_file:
            os.system('docker ps -a | grep myapp | awk \'{print $1}\' | xargs docker logs > ' + log_path)
            lines = log_file.readlines()
            for line in lines:
                if 'Serving Flask app "app"' in line:
                    app_healthy = True
                    break
    db_interaction = DbInteraction()
    db_interaction.add_user_info(
        username='test_q',
        email='qwe@mail.ru',
        password='test'
    )
    return lambda: print('App running!')


@pytest.fixture(scope='function')
def shutdown_app(request):
    log_path = request.config.getoption('--log_path')
    docker_compose_file = request.config.getoption('--docker_compose_file_path')
    log_writer_path = request.config.getoption('--log_writer_path')
    os.system(f'{log_writer_path} -f {log_path}')
    os.system(f'docker-compose --file {docker_compose_file} down')
    os.system('docker rmi project_vk_api_mock_server')
    return lambda: print('App shutdown!')


@dataclass
class ApiSettings:
    url: str = None
    username: str = None
    password: str = None
    log_path: str = None
    log_writer_path: str = None


@pytest.fixture(scope='session')
def config_api(request) -> ApiSettings:
    settings = ApiSettings(url=request.config.getoption('--url'), username=request.config.getoption('--username'),
                           password=request.config.getoption('--password'), log_path=request.config.getoption('--log_path'), log_writer_path=request.config.getoption('--log_writer_path'))
    return settings
