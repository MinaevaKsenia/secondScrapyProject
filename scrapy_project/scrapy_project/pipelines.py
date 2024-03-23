from sqlalchemy.orm import sessionmaker
from .model import db_connect, create_table, ForumData


class SaveForumDataPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        forum = ForumData()
        forum.title = item["title"]
        forum.username = item["usernames"]
        forum.date = item["dates"]
        forum.user_message = item["user_messages"]

        try:
            session.add(forum)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
