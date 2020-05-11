import pytest
import json

from http_server.utils.utils import get_key


@pytest.mark.SERVER
class TestServer:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, network_interaction):
        self.server, self.client = network_interaction

    def test_get_data(self):
        self.client.send_get_request('/data')
        data = self.client.get_response()['body']
        assert len(data['users']) == 2

    def test_get_user_by_id(self):
        user = {'name': 'Katya', 'surname': 'Ivanova'}
        self.client.send_post_request('/add_user', user)
        self.client.get_response()
        self.client.send_get_request('/data')
        data = self.client.get_response()['body']
        user_id = list(data['users'])[-1]
        assert data['users'][user_id] == user

    def test_add_user(self):
        user = {'name': 'Olya', 'surname': 'Petrova'}
        self.client.send_post_request('/add_user', user)
        response_data = self.client.get_response()['body']
        assert user == response_data

    def test_delete_user_by_id(self):
        user = {'name': 'Olya', 'surname': 'Petrova'}
        self.client.send_get_request('/data')
        data = self.client.get_response()['body']
        user_id = get_key(data['users'], user)
        self.client.send_delete_request(f'/delete_user/{user_id}')
        assert self.client.get_response()['body'] == user
