from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def db_connect():
    return create_engine("sqlite:///scrapy_forum.db")

def create_table(engine):
    Base.metadata.create_all(engine)

class ForumData(Base):
    __tablename__ = "forum"

    id = Column(Integer, primary_key=True)
    title = Column('title', String(200))
    username = Column('username', String)
    date = Column('date', String)
    user_message = Column('user_message', String)
