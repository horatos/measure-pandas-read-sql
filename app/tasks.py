from invoke import task
from tenacity import retry, stop_after_attempt, wait_fixed

from db import create_mysql_engine, create_postgres_engine
from initialize import initialize_mysql, initialize_postgres


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def check_connection():
    create_mysql_engine().connect()
    create_postgres_engine().connect()


@task
def init(c):
    check_connection()

    initialize_mysql(1000)
    initialize_postgres(1000)


if __name__ == '__main__':
    check_connection()
