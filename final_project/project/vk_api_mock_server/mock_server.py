import threading
import requests
import argparse

from flask import Flask, abort, request, jsonify
from mysql_models import TestUserVkId, TestUser
from mysql_client import MySQLConnection


class VkAPIMockServer:

    def __init__(self, host, port, mysql_connection: MySQLConnection):
        self.host = host
        self.port = port
        self.mysql_connection = mysql_connection
        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/data', view_func=self.get_data)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/vk_id/<username>', view_func=self.get_vk_id_by_username)
        self.app.add_url_rule('/set_vk_id', view_func=self.set_vk_id_by_username, methods=['POST'])
        self.app.add_url_rule('/change_vk_id', view_func=self.change_vk_id_by_username, methods=['POST'])
        self.app.add_url_rule('/delete_vk_id/<username>', view_func=self.delete_vk_id_by_username, methods=['DELETE'])

        self.app.register_error_handler(404, self.page_not_found)

    def page_not_found(self, err_description):
        if not str(err_description).endswith('User not found'):
            return jsonify(error=str(err_description)), 404
        else:
            return jsonify(), 404

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
        return 'Hello, vk api mock!'

    def get_data(self):
        test_users_vk_id = self.mysql_connection.session.query(TestUserVkId).all()
        if test_users_vk_id:
            data = dict()
            for test_user_vk_id in test_users_vk_id:
                self.mysql_connection.session.expire_all()
                data[test_user_vk_id.user.username] = test_user_vk_id.vk_id
            return data
        else:
            abort(404, description='Data not found')

    def get_vk_id_by_username(self, username):
        test_users_vk_id = self.mysql_connection.session.query(TestUserVkId).all()
        data = dict()
        for test_user_vk_id in test_users_vk_id:
            self.mysql_connection.session.expire_all()
            data[test_user_vk_id.user.username] = test_user_vk_id.vk_id
        vk_id = data.get(username, None)
        if vk_id is not None:
            return {'vk_id': vk_id}
        else:
            abort(404, description='User not found')

    def set_vk_id_by_username(self):
        request_body = dict(request.json)
        username = list(request_body.keys())[0]
        vk_id = request_body[username]
        try:
            user_id = self.mysql_connection.session.query(TestUser).filter_by(username=username).first().id
            test_user_vk_id = TestUserVkId(
                user_id=int(user_id),
                vk_id=vk_id
            )
            self.mysql_connection.session.add(test_user_vk_id)
            return f'Successful added user {username} with vk id: {vk_id}!', 201
        except IndexError:
            abort(404, description='Username not found')
        except AttributeError:
            abort(404, description='Username not found')

    def change_vk_id_by_username(self):
        request_body = dict(request.json)
        username = list(request_body.keys())[0]
        vk_id = request_body[username]
        try:
            user_id = self.mysql_connection.session.query(TestUser).filter_by(username=username).first().id
            user_vk_id = self.mysql_connection.session.query(TestUserVkId).filter_by(user_id=user_id).first()
            self.mysql_connection.session.expire_all()
            user_vk_id.vk_id = vk_id
            return f'Successful change user {username} info with vk id: {vk_id}!'
        except IndexError:
            abort(404, description='Username not found')

    def delete_vk_id_by_username(self, username):
        try:
            user_id = self.mysql_connection.session.query(TestUser).filter_by(username=username).first().id
            self.mysql_connection.session.query(TestUserVkId).filter_by(user_id=user_id).delete()
            return 'Successful deleted user vk id!', 204
        except IndexError:
            abort(404, description='Username not found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(type=str, dest='config')

    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = dict()
        lines = config_file.readlines()
        for line in lines:
            k, v = line.split(' = ')
            config[k] = v.split('\n')[0]

    mock_host = '0.0.0.0'
    mock_port = config['VK_URL'].split(':')[1]

    mysql_host = config['MYSQL_HOST']
    mysql_port = config['MYSQL_PORT']
    mysql_db_name = config['MYSQL_DB']

    mock = VkAPIMockServer(mock_host, mock_port, MySQLConnection(mysql_host, mysql_port, 'test_qa', 'qa_test', mysql_db_name))
    mock.run_mock()
