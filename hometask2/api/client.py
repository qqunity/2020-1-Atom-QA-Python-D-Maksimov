import requests
import json

from utils.exceptions import ResponseStatusCodeException
from urllib.parse import urljoin


class ApiClient:

    def __init__(self, config_api):
        self.base_url = config_api.url
        self.user_email = config_api.user_email
        self.user_password = config_api.user_password
        self.session = requests.Session()
        self.csrf_token = self.login()

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

    def login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'email': self.user_email,
            'password': self.user_password,
            'continue': 'https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com',
            'failure': 'https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com',
        }
        # Т.к. при переходи на ниже указанный url происходит большое кол-во редиректор, нам необходимо их повторить, чтобы забрать "печеньки" по каждой ссылке и CSRF токен на сессию
        url = 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0'
        response = self.make_request('POST', url, custom_location=True, json_convert=False, data=data, headers=headers,
                                     allow_redirects=False, status_code=302)

        # "Ручной" редирект на https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, data=data, headers=headers,
                                     allow_redirects=False, status_code=302)

        # "Ручной" редирект на https://account.my.com/sdc?token=4c7e4a95d4dae1a63bba33bd752231aa
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, data=data, headers=headers,
                                     allow_redirects=False, status_code=302)

        # "Ручной" редирект на https://auth-ac.my.com/sdc?from=https%3A%2F%2Ftarget.my.com%2Fcsrf%2F
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, data=data, headers=headers,
                                     allow_redirects=False, status_code=302)

        # "Ручной" редирект на https://target.my.com/sdc?token=61d9bfc3417323c708e877f11b898f0a
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, data=data, headers=headers,
                                     allow_redirects=False, status_code=302)

        # Получение сессионного CSRF
        url = 'https://target.my.com/csrf/'
        response = self.make_request('GET', url, custom_location=True, json_convert=False, allow_redirects=False,
                                     status_code=302)

        # "Ручной" редирект на https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, allow_redirects=False,
                                     status_code=302)

        # "Ручной" редирект на https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, allow_redirects=False,
                                     status_code=302)

        # "Ручной" редирект на https://auth-ac.my.com/sdc?from=https%3A%2F%2Faccount.my.com%2Flogin_continue%2F%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.com
        url = response.headers['location']
        response = self.make_request('GET', url, custom_location=True, json_convert=False, allow_redirects=False)

        return response.headers['set-cookie'].split('; ')[0].split('=')[1]

    def logout(self):
        headers = {
            'X-CSRFToken': self.csrf_token,
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }

        location = 'logout'

        responce = self.make_request('GET', location, headers=headers, json_convert=False)

    def create_new_segment(self, name):
        headers = {
            'X-CSRFToken': self.csrf_token,
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }

        json_data = {
            'name': name,
            'pass_condition': 1,
            'relations':
                [
                    {
                        'object_type': 'remarketing_player',
                        'params':
                            {
                                'type': 'positive',
                                'left': 365,
                                'right': 0
                            }
                    },
                    {
                        'object_type': 'remarketing_payer',
                        'params':
                            {
                                'type': 'positive',
                                'left': 365,
                                'right': 0
                            }
                    }
                ],
            'logicType': 'or'
        }

        location = 'api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,flags'

        response = self.make_request('POST', location, headers=headers, json=json_data)

        return response['id']

    def delete_segment(self, segment_id):
        segment_exists = False
        for segment in self.get_segments_list():
            if segment['id'] == segment_id:
                segment_exists = True
        if segment_exists:
            headers = {
                'X-CSRFToken': self.csrf_token,
                'Referer': 'https://target.my.com/segments/segments_list/new',
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }

            location = 'api/v2/remarketing/segments/' + str(segment_id) + '.json'

            response = self.make_request('DELETE', location, headers=headers, json_convert=False, status_code=204)

    def get_segments_list(self):
        location = 'api/v2/remarketing/segments.json'
        response = self.make_request('GET', location)
        return response['items']

    def rename_segment(self, new_name, segment_id):
        headers = {
            'X-CSRFToken': self.csrf_token,
            'Referer': 'https://target.my.com/segments/segments_list/new',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }

        json_data = {
            'name': new_name,
            'pass_condition': 1,
            'relations':
                [
                    {
                        'object_type': 'remarketing_player',
                        'params':
                            {
                                'type': 'positive',
                                'left': 365,
                                'right': 0
                            }
                    },
                    {
                        'object_type': 'remarketing_payer',
                        'params':
                            {
                                'type': 'positive',
                                'left': 365,
                                'right': 0
                            }
                    }
                ],
            'logicType': 'or'
        }

        location = 'api/v2/remarketing/segments/' + str(segment_id) + '.json'

        response = self.make_request('POST', location, headers=headers, json=json_data, status_code=204,
                                     json_convert=False)

    def delete_all_segments(self, segments):
        for segment in segments:
            self.delete_segment(segment['id'])
