import pytest

from api.client import ApiClient


@pytest.fixture(scope='session')
def built_api_client(config_api):
    return ApiClient(config_api)


@pytest.fixture(scope='function')
def create_temp_segment_with_api(built_api_client):
    api_client = built_api_client
    tmp_segment_id = api_client.create_new_segment('Test1')

    yield api_client, tmp_segment_id

    api_client.delete_all_segments(api_client.get_segments_list())
