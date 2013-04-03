from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'cloudbeer'
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String, nullable=False)
    nick = Column(String)
    password = Column(String, nullable=False)
    salt = Column(String)
    login_time = Column(DateTime)
    status = Column(Integer, default=1)
    create_date = Column(DateTime)

    def __init__(self, id=None, email=None, nick=None, password=None, salt=None, login_time=None, status=None,
                 create_date=None):
        self.id = id
        self.email = email
        self.nick = nick
        self.password = password
        self.salt = salt
        self.login_time = login_time
        self.status = status
        self.create_date = create_date

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.id, self.email, self.nick)


class Template(Base):
    __tablename__ = "template"

    id = Column(Integer, Sequence('template_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, default=0)
    content = Column(String)
    status = Column(Integer, default=1)
    type = Column(Integer, default=1)
    popular = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    create_date = Column(DateTime)

    def __init__(self, id, title, user_id, content, status, type, popular, rank, create_date):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.content = content
        self.type = type
        self.popular = popular
        self.rank = rank
        self.status = status
        self.create_date = create_date

    def __repr__(self):
        return "<Template('%s','%s', '%s', '%s')>" % (self.id, self.title, self.popular, self.rank)


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, Sequence('project_id_seq'), primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, default=0)
    content = Column(String)
    status = Column(Integer, default=1)
    create_date = Column(DateTime)

    def __init__(self, id=None, title=None, user_id=None, content=None, status=None, create_date=None):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.content = content
        self.status = status
        self.create_date = create_date

    def __repr__(self):
        return "<User('%s','%s')>" % (self.id, self.title)