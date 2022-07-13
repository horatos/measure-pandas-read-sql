import logging

from invoke import task
from tenacity import retry, stop_after_attempt, wait_fixed

from db import create_mysql_engine, create_postgres_engine, create_db_engine
from initialize import initialize_mysql, initialize_postgres
from experiments import *


logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(20), wait=wait_fixed(3))
def check_connection():
    create_mysql_engine().connect()
    create_postgres_engine().connect()


@task
def init(c, nrows):
    logger.info("Start waiting databases initialization")
    check_connection()
    logger.info("Done waiting databases initialization")

    nrows = int(nrows)
    mysql_nrows = initialize_mysql(nrows)
    pg_nrows = initialize_postgres(nrows)

    if mysql_nrows != pg_nrows:
        raise Exception("MySQL nrows is not equal to PostgreSQL nrows")


@task
def exp1(c, db):
    exec_experiment_1(db)


@task
def exp2(c, db, chunksize):
    exec_experiment_2(db, chunksize)


if __name__ == '__main__':
    check_connection()
