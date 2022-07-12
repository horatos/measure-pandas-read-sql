import logging

from invoke import task
from tenacity import retry, stop_after_attempt, wait_fixed

from db import create_mysql_engine, create_postgres_engine
from initialize import initialize_mysql, initialize_postgres


logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def check_connection():
    create_mysql_engine().connect()
    create_postgres_engine().connect()


@task
def init(c, nrows):
    logger.info("Start waiting databases initialization")
    check_connection()
    logger.info("Done waiting databases initialization")

    nrows = int(nrows)
    initialize_mysql(nrows)
    initialize_postgres(nrows)


if __name__ == '__main__':
    check_connection()
