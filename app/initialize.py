import logging
import random
import string

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from db import create_mysql8_engine, create_postgres_engine


logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(240))

    def __repr__(self):
        return f"User(id={self.id!r},name={self.name!r})"


def random_string(length: int) -> str:
    return ''.join((random.choice(string.printable) for _ in range(length)))

def initialize_table(engine, nrows: int) -> int:
    Session = sessionmaker(engine)

    Base.metadata.create_all(engine)

    with Session() as session:
        for i in range(nrows):
            name = random_string(240)
            user = User(name=name)
            session.add(user)
        session.commit()

    with Session() as session:
        added_rows = session.query(User).count()
        session.commit()

    return added_rows


def initialize_mysql8(nrows: int) -> int:
    """Initialize MySQL database with random records."""

    engine = create_mysql8_engine()

    logger.info("Start adding %s rows", nrows)
    added_rows = initialize_table(engine, nrows)
    logger.info("Added rows count = %s", added_rows)

    return added_rows


def initialize_postgres(nrows: int) -> int:
    """Initialize PostgreSQL database with random records."""

    engine = create_postgres_engine()

    logger.info("Start adding %s rows", nrows)
    added_rows = initialize_table(engine, nrows)
    logger.info("Added rows count = %s", added_rows)

    return added_rows
