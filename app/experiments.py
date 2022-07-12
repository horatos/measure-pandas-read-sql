import logging

import pandas as pd
from memory_profiler import profile

from db import create_db_engine


logger = logging.getLogger(__name__)


@profile
def exec_experiment_1(db: str):
    logger.info("Execute the experiment#1 with db(%s)", db)

    engine = create_db_engine(db)
    dataframe = pd.read_sql("SELECT * FROM users", engine)

    logger.info("Got %s records", len(dataframe))
