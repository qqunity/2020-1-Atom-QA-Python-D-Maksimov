from vk_api_client.http_client import HttpClient
from vk_api_client.utils import get_vk_api_mock_server_info


class VkApiClient:

    def __init__(self):
        self.host, self.port = get_vk_api_mock_server_info()
        self.http_client = HttpClient(self.host, self.port)
        self.http_client.open_connection()

    def get_home_page_info(self):
        self.http_client.send_get_request('/')
        return self.http_client.get_response()

    def get_vk_id_by_username(self, username):
        self.http_client.send_get_request(f'/vk_id/{username}')
        return self.http_client.get_response()

    def get_data(self):
        self.http_client.send_get_request('/data')
        return self.http_client.get_response()

    def shutdown_mock(self):
        self.http_client.send_get_request('/shutdown')
        self.http_client.close_connection()

    def set_vk_id_by_username(self, data):
        self.http_client.send_post_request('/set_vk_id', data)
        return self.http_client.get_response()

    def change_vk_id_by_username(self, data):
        self.http_client.send_post_request('/change_vk_id', data)
        return self.http_client.get_response()

    def delete_vk_id_by_username(self, username):
        self.http_client.send_delete_request(f'/delete_vk_id/{username}')
        return self.http_client.get_response()

    def close_connection(self):
        self.http_client.close_connection()
