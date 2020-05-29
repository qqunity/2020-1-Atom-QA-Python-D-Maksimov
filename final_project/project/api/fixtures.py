import pytest

from api.client import ApiClient
from api.utils.exceptions import ResponseStatusCodeException


@pytest.fixture(scope='session')
def get_api_client(config_api):
    return ApiClient(config_api)


@pytest.fixture(scope='function')
def add_fake_user(get_api_client, get_fake_user_info):
    api_client = get_api_client
    api_client.login()
    username, password, email = get_fake_user_info
    api_client.add_user(
        username=username,
        password=password,
        email=email,
        status_code=210
    )
    yield username
    try:
        api_client.del_user(username)
        api_client.logout()
    except ResponseStatusCodeException:
        api_client.logout()
