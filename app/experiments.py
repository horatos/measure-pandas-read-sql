import logging

import pandas as pd
from memory_profiler import profile

from db import create_db_engine


logger = logging.getLogger(__name__)


@profile
def exec_experiment_1(db: str):
    logger.info("Execute the experiment#1 with db = %s", db)

    conn = create_db_engine(db).connect()
    dataframe = pd.read_sql("SELECT * FROM users", conn)

    logger.info("Got %s records", len(dataframe))


@profile
def exec_experiment_2(db: str, chunksize: int):
    logger.info("Execute the experiment#2 with db = %s, chunksize = %s", db, chunksize)
    total = 0
    chunksize = int(chunksize)

    conn = create_db_engine(db).connect()
    it = pd.read_sql("SELECT * FROM users", conn, chunksize=chunksize)
    for chunk in it:
        total += len(chunk)

    logger.info("Got %s records", total)


@profile
def exec_experiment_3(db: str):
    logger.info("Execute the experiment#3 with db = %s", db)

    conn = create_db_engine(db).connect().execution_options(stream_results=True)
    dataframe = pd.read_sql("SELECT * FROM users", conn)

    logger.info("Got %s records", len(dataframe))

