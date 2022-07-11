from invoke import task
from tenacity import retry, stop_after_attempt, wait_fixed

from db import create_mysql_engine
from initialize import initialize_mysql


@task
def init(c):
    initialize_mysql(1000)


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def check_mysql_connection():
    create_mysql_engine().connect()


if __name__ == '__main__':
    check_mysql_connection()
