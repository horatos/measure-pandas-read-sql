import logging

import pandas as pd
from memory_profiler import profile


logger = logging.getLogger(__name__)


@profile
def exec_experiment_1(engine):
    logger.info("Execute the experiment#1")

    dataframe = pd.read_sql("SELECT * FROM users", engine)

    logger.info("Got %s records", len(dataframe))
