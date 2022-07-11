import logging
import random
import string

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from db import create_mysql_engine


logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(240))

    def __repr__(self):
        return f"User(id={self.id!r},name={self.name!r})"


def random_string(length):
    return ''.join((random.choice(string.printable) for _ in range(length)))

def initialize_mysql(nrows):
    engine = create_mysql_engine()
    Session = sessionmaker(engine)

    Base.metadata.create_all(engine)

    with Session() as session:
        for i in range(nrows+1):
            name = random_string(240)
            user = User(id=i, name=name)
            session.merge(user)
        session.commit()

    with Session() as session:
        added_rows = session.query(User).count()
        session.commit()

    logger.info("Added rows count = %s", added_rows)
