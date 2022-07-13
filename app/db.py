from sqlalchemy import create_engine


def create_mysql8_engine():
    return create_engine("mysql+pymysql://root:rootpass@mysql8/example")


def create_postgres_engine():
    return create_engine("postgresql+psycopg2://postgres:rootpass@postgres/example")


def create_db_engine(db: str):
    if db.lower() == "mysql8":
        return create_mysql8_engine()
    elif db.lower() == "postgres" or db.lower() == "postgresql":
        return create_postgres_engine()
    else:
        raise Exception(f"Unknown database name: {db}")
