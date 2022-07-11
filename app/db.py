from sqlalchemy import create_engine


def create_mysql_engine():
    return create_engine("mysql+pymysql://root:rootpass@mysql/example")
