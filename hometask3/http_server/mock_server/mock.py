import threading
import requests

from flask import Flask, abort, request, jsonify


class MockServer:

    def __init__(self, host, port, data=None):
        self.host = host
        self.port = port
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/data', view_func=self.get_data)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/user/<user_id>', view_func=self.get_user_by_id)
        self.app.add_url_rule('/add_user', view_func=self.add_user, methods=['POST'])
        self.app.add_url_rule('/delete_user/<user_id>', view_func=self.delete_user_by_id, methods=['DELETE'])

    def run_mock(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def shutdown_mock(self):
        requests.get(f'http://{self.host}:{self.port}/shutdown')

    def shutdown(self):
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    def get_home(self):
        return 'Hello, mock!'

    def get_data(self):
        if self.data:
            return self.data
        else:
            abort(404)

    def get_user_by_id(self, user_id: int):
        user = self.data['users'].get(str(user_id), None)
        if user is None:
            abort(404)
        else:
            return user

    def add_user(self):
        last_id = int(list(self.data['users'])[-1])
        self.data['users'][str(last_id + 1)] = dict(request.json)
        return request.json

    def delete_user_by_id(self, user_id):
        user = self.data['users'].get(str(user_id), None)
        if user is None:
            abort(404)
        else:
            del self.data['users'][str(user_id)]
            return user


if __name__ == '__main__':
    mock = MockServer('127.0.0.1', 5000,
                      data={'users': {
                          '1': {'name': 'Denis', 'surname': 'Maksimov'},
                          '2': {'name': 'Petya', 'surname': 'Ivanov'}
                      }
                      })
    mock.run_mock()
