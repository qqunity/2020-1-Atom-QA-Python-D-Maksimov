import os

from database_code.models.models import Base, RequestUrl, RequestIPAddress, LogInfo
from database_code.mysql_client.client import MySQLConnection
from database_code.utils.utils import get_uniq_ip_addresses, get_uniq_urls
from tqdm import tqdm


class MySQLBuilder:

    def __init__(self, connection: MySQLConnection, rebuild_db=True):
        self.connection = connection
        self.engine = connection.connection.engine
        if rebuild_db:
            self.create_req_ip_addresses()
            self.create_req_urls()
            self.create_logs_info()

    def create_req_urls(self):
        if not self.engine.dialect.has_table(self.engine, 'req_urls'):
            Base.metadata.tables['req_urls'].create(self.engine)
        else:
            self.connection.execute_query('DROP TABLE IF EXISTS req_urls')
            Base.metadata.tables['req_urls'].create(self.engine)

    def create_req_ip_addresses(self):
        if not self.engine.dialect.has_table(self.engine, 'req_ip_addresses'):
            Base.metadata.tables['req_ip_addresses'].create(self.engine)
        else:
            self.connection.execute_query('DROP TABLE IF EXISTS req_ip_addresses')
            Base.metadata.tables['req_ip_addresses'].create(self.engine)

    def create_logs_info(self):
        if not self.engine.dialect.has_table(self.engine, 'logs_info'):
            Base.metadata.tables['logs_info'].create(self.engine)
        else:
            self.connection.execute_query('DROP TABLE IF EXISTS logs_info')
            Base.metadata.tables['logs_info'].create(self.engine)

    def fill_database(self, log_path):
        if not os.path.isdir(log_path):
            with open(log_path, 'r') as log_file:
                lines = log_file.readlines()
                u_ip_addresses = get_uniq_ip_addresses(lines)
                for ip_address in tqdm(u_ip_addresses):
                    ip_add = RequestIPAddress(
                        ip=ip_address
                    )
                    self.connection.session.add(ip_add)
                u_urls = get_uniq_urls(lines)
                for u_url in tqdm(u_urls):
                    url = RequestUrl(
                        url=u_url
                    )
                    self.connection.session.add(url)
                req_urls = self.connection.session.query(RequestUrl).all()
                req_ip_addresses = self.connection.session.query(RequestIPAddress).all()
                for line in tqdm(lines):
                    cur_req_url = line.split()[6]
                    cur_req_ip_addresses = line.split()[0]
                    for req_url in req_urls:
                        if req_url.url == cur_req_url:
                            req_url_id = req_url.id
                            break
                    for req_ip_address in req_ip_addresses:
                        if req_ip_address.ip == cur_req_ip_addresses:
                            req_ip_address_id = req_ip_address.id
                            break
                    log = LogInfo(
                        req_ip_address_id=req_ip_address_id,
                        req_url_id=req_url_id,
                        req_method=line.split()[5][1:],
                        response_code=int(line.split()[8]),
                        req_size=int(line.split()[9])
                    )
                    self.connection.session.add(log)
                self.connection.session.commit()

        else:
            for log in os.listdir(log_path):
                with open(os.path.join(log_path, log), 'r') as log_file:
                    lines = log_file.readlines()
                    u_ip_addresses = get_uniq_ip_addresses(lines)
                    u_ip_addresses_from_db = self.connection.session.query(RequestIPAddress).all()
                    u_ip_addresses_from_db = list(map(lambda ip_add: ip_add.ip, u_ip_addresses_from_db))
                    if u_ip_addresses_from_db:
                        u_ip_addresses = list(set(u_ip_addresses) - set(u_ip_addresses_from_db))
                    for ip_address in tqdm(u_ip_addresses):
                        ip_add = RequestIPAddress(
                            ip=ip_address
                        )
                        self.connection.session.add(ip_add)
                    u_urls = get_uniq_urls(lines)
                    u_urls_from_db = self.connection.session.query(RequestUrl).all()
                    u_urls_from_db = list(map(lambda url: url.url, u_urls_from_db))
                    if u_urls_from_db:
                        u_urls = list(set(u_urls) - set(u_urls_from_db))
                    for u_url in tqdm(u_urls):
                        url = RequestUrl(
                            url=u_url
                        )
                        self.connection.session.add(url)
                req_urls = self.connection.session.query(RequestUrl).all()
                req_ip_addresses = self.connection.session.query(RequestIPAddress).all()
                for line in tqdm(lines):
                    cur_req_url = line.split()[6]
                    cur_req_ip_addresses = line.split()[0]
                    for req_url in req_urls:
                        if req_url.url == cur_req_url:
                            req_url_id = req_url.id
                            break
                    for req_ip_address in req_ip_addresses:
                        if req_ip_address.ip == cur_req_ip_addresses:
                            req_ip_address_id = req_ip_address.id
                            break
                    log = LogInfo(
                        req_ip_address_id=req_ip_address_id,
                        req_url_id=req_url_id,
                        req_method=line.split()[5][1:],
                        response_code=int(line.split()[8]),
                        req_size=int(line.split()[9])
                    )
                    self.connection.session.add(log)
            self.connection.session.commit()

    def add_log_info(self, log_info):
        raw_log_info = log_info.split()
        cur_req_ip_address = raw_log_info[0]
        cur_req_url = raw_log_info[6]
        cur_req_method = raw_log_info[5][1:]
        cur_response_code = int(raw_log_info[8])
        cur_req_size = int(raw_log_info[9])
        u_ip_addresses_from_db = self.connection.session.query(RequestIPAddress).all()
        u_ip_addresses_from_db = list(map(lambda ip_add: ip_add.ip, u_ip_addresses_from_db))
        if not cur_req_ip_address in u_ip_addresses_from_db:
            ip_add = RequestIPAddress(
                ip=cur_req_ip_address
            )
            self.connection.session.add(ip_add)
        u_urls_from_db = self.connection.session.query(RequestUrl).all()
        u_urls_from_db = list(map(lambda url: url.url, u_urls_from_db))
        if not cur_req_url in u_urls_from_db:
            url = RequestUrl(
                url=cur_req_url
            )
            self.connection.session.add(url)
        req_urls = self.connection.session.query(RequestUrl).all()
        req_ip_addresses = self.connection.session.query(RequestIPAddress).all()
        for req_url in req_urls:
            if req_url.url == cur_req_url:
                req_url_id = req_url.id
                break
        for req_ip_address in req_ip_addresses:
            if req_ip_address.ip == cur_req_ip_address:
                req_ip_address_id = req_ip_address.id
                break
        log = LogInfo(
            req_ip_address_id=req_ip_address_id,
            req_url_id=req_url_id,
            req_method=cur_req_method,
            response_code=cur_response_code,
            req_size=cur_req_size
        )
        self.connection.session.add(log)
        self.connection.session.commit()
        return log
