import os


def get_db_host():
    return os.popen('./project/database_code/get_db_host').read().split('\n')[0]


def get_db_name():
    with open('./project/app_config/config.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.split(' = ')[0] == 'MYSQL_DB':
                return line.split(' = ')[1].split('\n')[0]


def get_db_port():
    with open('./project/app_config/config.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.split(' = ')[0] == 'MYSQL_PORT':
                return line.split(' = ')[1].split('\n')[0]