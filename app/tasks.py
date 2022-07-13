import logging

from invoke import task
from tenacity import retry, stop_after_attempt, wait_fixed

from db import *
from initialize import *
from experiments import *


logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(20), wait=wait_fixed(3))
def check_connection():
    create_mysql8_engine().connect()
    create_mysql57_engine().connect()
    create_postgres_engine().connect()


@task
def init(c, nrows):
    logger.info("Start waiting databases initialization")
    check_connection()
    logger.info("Done waiting databases initialization")

    nrows = int(nrows)
    mysql8_nrows = initialize_mysql8(nrows)
    mysql57_nrows = initialize_mysql57(nrows)
    pg_nrows = initialize_postgres(nrows)

    if mysql8_nrows != pg_nrows or mysql57_nrows != pg_nrows:
        raise Exception("MySQL nrows is not equal to PostgreSQL nrows")


@task
def exp1(c, db):
    exec_experiment_1(db)


@task
def exp2(c, db, chunksize):
    exec_experiment_2(db, chunksize)


@task
def exp3(c, db):
    exec_experiment_3(db)


@task
def exp4(c, db, chunksize):
    exec_experiment_4(db, chunksize)


if __name__ == '__main__':
    check_connection()
