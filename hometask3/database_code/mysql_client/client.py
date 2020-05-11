import sqlalchemy

from sqlalchemy.orm import sessionmaker


class MySQLConnection:

    def __init__(self, user, password, db_name, rebuild_db=True):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '127.0.0.1'
        self.port = 3306

        self.rebuild_db = rebuild_db
        self.connection = self.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name if db_created else ""}',
            encoding='utf8'
        )
        return engine.connect()

    def connect(self):
        connection = self.get_connection()
        if self.rebuild_db:
            connection.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
            connection.execute(f'CREATE DATABASE {self.db_name}')
            connection.close()
        return self.get_connection(db_created=True)

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res
