from sqlalchemy import create_engine


def create_mysql_engine():
    return create_engine("mysql+pymysql://root:rootpass@mysql/example")

def create_postgres_engine():
    return create_engine("postgresql+psycopg2://postgres:rootpass@postgres/example")
