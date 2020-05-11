import argparse

from sqlalchemy import desc, func
from database_code.models.models import LogInfo, RequestUrl, RequestIPAddress
from database_code.mysql_client.client import MySQLConnection
from database_code.tests.builder import MySQLBuilder
from python_scripts.exceptions import ParamsException, CommandNotFoundException


def mysql_client(rebuild_db):
    return MySQLConnection('root', 'pass', 'nginx_logs', rebuild_db=rebuild_db)


class LogProcessing:

    def __init__(self, log_path, rebuild_db=True):
        self.mysql: MySQLConnection = mysql_client(rebuild_db)
        self.builder = MySQLBuilder(self.mysql, rebuild_db=rebuild_db)
        if rebuild_db:
            self.builder.fill_database(log_path)

    def run_cmd1(self):
        print(f'{len(self.mysql.session.query(LogInfo).all())} lines in log file')

    def run_cmd2(self, req_type):
        if not req_type:
            raise ParamsException('Invalid count of parameters!')
        print(f'Count of {req_type} requests is equal {len(self.mysql.session.query(LogInfo).filter_by(req_method=req_type).all())}')

    def run_cmd3(self):
        query = self.mysql.session.query(LogInfo).order_by(desc(LogInfo.req_size)).limit(10)
        req_urls = list(map(lambda req_url: req_url.url, self.mysql.session.query(RequestUrl).all()))
        req_ip_addresses = list(map(lambda req_id_address: req_id_address.ip, self.mysql.session.query(RequestIPAddress)))
        for line in query:
            print(f'{req_ip_addresses[line.req_ip_address_id - 1]} {req_urls[line.req_url_id - 1]} {line.req_method} {line.response_code} {line.req_size}')

    def run_cmd4(self):
        query = self.mysql.session.query(LogInfo.req_url_id, LogInfo.response_code, func.count()).filter(LogInfo.response_code.like('4%')).order_by(desc(func.count())).group_by(LogInfo.req_url_id, LogInfo.response_code).all()
        req_urls = list(map(lambda req_url: req_url.url, self.mysql.session.query(RequestUrl).all()))
        for line in query:
            print(f'{req_urls[line[0] - 1]} status_code:{line[1]} is repeated {line[2]} times')

    def run_cmd5(self):
        query = self.mysql.session.query(LogInfo.req_ip_address_id, LogInfo.req_url_id, LogInfo.response_code, LogInfo.req_size).filter(LogInfo.response_code.like('4%')).order_by(desc(LogInfo.req_size)).distinct().limit(10).all()
        req_urls = list(map(lambda req_url: req_url.url, self.mysql.session.query(RequestUrl).all()))
        req_ip_addresses = list(map(lambda req_id_address: req_id_address.ip, self.mysql.session.query(RequestIPAddress)))
        for line in query:
            print(f'{req_ip_addresses[line[0] - 1]} {req_urls[line[1] - 1]} status_code:{line[2]} {line[3]}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_path', type=str, dest='log_path')
    parser.add_argument('--cmd', type=int, dest='cmd')
    parser.add_argument('--req_type', type=str, dest='req_type')

    args = parser.parse_args()

    log_p = LogProcessing(args.log_path, rebuild_db=False)
    if args.cmd == 1:
        log_p.run_cmd1()
    elif args.cmd == 2:
        log_p.run_cmd2(args.req_type)
    elif args.cmd == 3:
        log_p.run_cmd3()
    elif args.cmd == 4:
        log_p.run_cmd4()
    elif args.cmd == 5:
        log_p.run_cmd5()
    else:
        raise CommandNotFoundException('Command not found!')