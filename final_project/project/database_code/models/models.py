from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, SMALLINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TestUser(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SMALLINT, nullable=True)
    active = Column(SMALLINT, nullable=True)
    start_active_time = Column(DateTime, nullable=True)
    UniqueConstraint(username, name='ix_test_users_username')
    UniqueConstraint(email, name='email')

    def __repr__(self):
        return f"<TestUser(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'" \
               f")>"


class TestUserVkId(Base):
    __tablename__ = 'test_users_vk_id'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey(f'{TestUser.__tablename__}.{TestUser.id.name}'), nullable=False)
    vk_id = Column(VARCHAR(50), nullable=True)
    user = relationship('TestUser', backref='vk_id')

    def __repr__(self):
        return f"<ReqIPAdress(" \
               f"id='{self.id}'," \
               f"user_id='{self.user.id}'," \
               f"vk_id='{self.vk_id}'" \
               f")>"
