from database_code.models.models import TestUser
from database_code.mysql_client.client import MySQLConnection
from database_code.utils.exceptions import IncorrectUsernameException, IncorrectEmailException, \
    IncorrectPasswordException, UserNotFoundException
from database_code.utils.utils import get_db_name, get_db_host, get_db_port

import requests


class DbInteraction:

    def __init__(self, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=get_db_host(),
            port=get_db_port(),
            user='test_qa',
            password='qa_test',
            db_name=get_db_name(),
            rebuild_db=rebuild_db
        )

    def add_user_info(self, username, email, password):
        if len(username) <= 5 or len(username) > 16:
            raise IncorrectUsernameException('Incorrect username length')
        if '@' not in email or '.' not in email.split('@')[1] or len(email.split('@')[1]) < 3 or len(email) > 64:
            raise IncorrectEmailException('Invalid email address')
        if len(password) > 255:
            raise IncorrectPasswordException('Incorrect password length')
        test_user = TestUser(
            username=username,
            password=password,
            email=email,
            access=1,
            active=0
        )
        self.mysql_connection.session.add(test_user)
        return self.get_user_info(username)

    def del_user_info(self, username):
        if self.mysql_connection.session.query(TestUser).filter_by(username=username).all():
            self.mysql_connection.session.query(TestUser).filter_by(username=username).delete()
        else:
            raise UserNotFoundException('User not found')

    def get_user_info(self, username):
        try:
            user_info = self.mysql_connection.session.query(TestUser).filter_by(username=username).all()[0]
            self.mysql_connection.session.expire_all()
            return {'username': user_info.username, 'email': user_info.email, 'password': user_info.password, 'active': user_info.active, 'access': user_info.access, 'start_active_time': user_info.start_active_time}
        except IndexError:
            raise UserNotFoundException('User not found')

    def edit_user_info(self, username,  new_username=None, new_email=None, new_password=None, new_access=None, new_active=None):
        user_info = self.mysql_connection.session.query(TestUser).filter_by(username=username).first()
        if user_info:
            if new_username is not None:
                if len(new_username) <= 5 or len(new_username) > 16:
                    raise IncorrectUsernameException('Incorrect username length')
                else:
                    user_info.username = new_username
            if new_email is not None:
                if '@' not in new_email or '.' not in new_email.split('@')[1] or len(new_email.split('@')[1]) < 3 or len(new_email) > 64:
                    raise IncorrectEmailException('Invalid email address')
                else:
                    user_info.email = new_email
            if new_password is not None:
                if len(new_password) > 255:
                    raise IncorrectPasswordException('Incorrect password length')
                else:
                    user_info.password = new_password
            if new_access is not None:
                user_info.access = new_access
            if new_active is not  None:
                user_info.active = new_active
            return self.get_user_info(username)
        else:
            raise UserNotFoundException('User not found')

    def get_all_users_info(self):
        users = list(map(lambda user_info: user_info.username, self.mysql_connection.session.query(TestUser).all()))
        users_info = dict()
        for user in users:
            users_info[user] = self.get_user_info(user)
        return users_info
