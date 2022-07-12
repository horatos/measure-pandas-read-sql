from sqlalchemy import create_engine


def create_mysql_engine():
    return create_engine("mysql+pymysql://root:rootpass@mysql/example")


def create_postgres_engine():
    return create_engine("postgresql+psycopg2://postgres:rootpass@postgres/example")


def create_db_engine(db: str):
    if db.lower() == "mysql":
        return create_mysql_engine()
    elif db.lower() == "postgres" or db.lower() == "postgresql":
        return create_postgres_engine()
    else:
        raise Exception(f"Unknown database name: {db}")
