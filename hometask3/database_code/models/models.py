from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RequestUrl(Base):
    __tablename__ = 'req_urls'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<ReqUrl(" \
               f"id='{self.id}'," \
               f"url='{self.url}'" \
               f")>"


class RequestIPAddress(Base):
    __tablename__ = 'req_ip_addresses'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<ReqIPAdress(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'" \
               f")>"


class LogInfo(Base):
    __tablename__ = 'logs_info'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    req_url_id = Column(Integer, ForeignKey(f'{RequestUrl.__tablename__}.{RequestUrl.id.name}'), nullable=False)
    req_url = relationship('RequestUrl', backref='logs_info')
    req_method = Column(String(10), nullable=False)
    response_code = Column(Integer, nullable=False)
    req_size = Column(Integer, nullable=False)
    req_ip_address_id: Column = Column(Integer,
                                       ForeignKey(f'{RequestIPAddress.__tablename__}.{RequestIPAddress.id.name}'),
                                       nullable=False)
    req_ip_address = relationship('RequestIPAddress', backref='logs_info')

    def __repr__(self):
        return f"<LogInfo(" \
               f"id='{self.id}'," \
               f"req_ip_address='{self.req_ip_address.ip}'," \
               f"req_url='{self.req_url.url}'," \
               f"req_method='{self.req_method}'," \
               f"response_code='{self.response_code}'," \
               f"req_size='{self.req_size}'," \
               f")>"
