import requests
import json

from urllib.parse import urljoin

from api.utils.exceptions import ResponseStatusCodeException


class ApiClient:

    def __init__(self, config_api):
        self.base_url = config_api.url
        self.username = config_api.username
        self.password = config_api.password
        self.session = requests.Session()

    def make_request(self, method, location, status_code=200, headers=None, params=None, data=None, json_convert=True,
                     custom_location=False, allow_redirects=True, json=None):
        if not custom_location:
            url = urljoin(self.base_url, location)
        else:
            url = location

        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects, json=json)

        if response.status_code != status_code:
            raise ResponseStatusCodeException(f' Got {response.status_code} {response.reason} for URL "{url}"')
        if json_convert:
            json_response = response.json()
            return json_response
        return response

    def login(self, username=None, password=None, status_code=None):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://127.0.0.1:8080/login'
        }

        data = {
            'username': self.username if username is None else username,
            'password': self.password if password is None else password,
            'submit': 'login'
        }

        location = 'login'
        response = self.make_request('POST', location, json_convert=False, data=data, headers=headers, allow_redirects=False, status_code=302 if status_code is None else status_code)
        return response

    def reg_user(self, username, password, confirm_password, email, status_code=None, autoremove=False):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://127.0.0.1:8080/reg'
        }

        data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm': confirm_password,
            'term': 'y',
            'submit': 'Register'
        }

        location = 'reg'
        try:
            response = self.make_request('POST', location, json_convert=False, data=data, headers=headers, allow_redirects=False, status_code=201 if status_code is None else status_code)
        except ResponseStatusCodeException as exception:
            if autoremove:
                self.del_user(username)
            raise exception
        if autoremove:
            self.del_user(username)
        return response

    def add_user(self, username, password, email, status_code=None, autoremove=False):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'username': username,
            'password': password,
            'email': email
        }

        location = 'api/add_user'
        try:
            response = self.make_request('POST', location, json_convert=False, headers=headers, allow_redirects=False, json=data, status_code=201 if status_code is None else status_code)
        except ResponseStatusCodeException as exception:
            if autoremove:
                self.del_user(username)
            raise exception
        if autoremove:
            self.del_user(username)
        return response

    def block_user(self, username, status_code=None):
        location = f'api/block_user/{username}'
        response = self.make_request('GET', location, json_convert=False, status_code=200 if status_code is None else status_code)
        return response

    def accept_user(self, username, status_code=None):
        location = f'api/accept_user/{username}'
        response = self.make_request('GET', location, json_convert=False, status_code=200 if status_code is None else status_code)
        return response

    def del_user(self, username, status_code=None):
        location = f'api/del_user/{username}'
        response = self.make_request('GET', location, json_convert=False, status_code=204 if status_code is None else status_code)
        return response

    def get_app_status(self, status_code=None):
        location = 'status'
        response = self.make_request('GET', location, status_code=200 if status_code is None else status_code)
        return response

    def logout(self, status_code=None):
        location = 'logout'
        response = self.make_request('GET', location, json_convert=False, status_code=200 if status_code is None else status_code)
        return response
