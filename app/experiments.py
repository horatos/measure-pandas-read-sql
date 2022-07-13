import logging

import pandas as pd
from memory_profiler import profile

from db import create_db_engine


logger = logging.getLogger(__name__)


@profile
def exec_experiment_1(db: str):
    logger.info("Execute the experiment#1 with db = %s", db)

    engine = create_db_engine(db)
    dataframe = pd.read_sql("SELECT * FROM users", engine)

    logger.info("Got %s records", len(dataframe))


@profile
def exec_experiment_2(db: str, chunksize: int):
    logger.info("Execute the experiment#1 with db = %s, chunksize = %s", db, chunksize)
    total = 0
    chunksize = int(chunksize)

    engine = create_db_engine(db)
    it = pd.read_sql("SELECT * FROM users", engine, chunksize=chunksize)
    for chunk in it:
        total += len(chunk)

    logger.info("Got %s records", total)
