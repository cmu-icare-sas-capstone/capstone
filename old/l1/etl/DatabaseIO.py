import threading
import pandas as pd
from old.utils.MySQLEngine import mysql_engine
from pandas import DataFrame
import old.l1.constants.FILEPATH as FILEPATH


class DatabaseIO(threading.Thread):
    batch_num = 0

    def __init__(self, df: DataFrame, table_name: str, tread_id: int):
        threading.Thread.__init__(self)
        self.thread_id = tread_id
        self.db_connection = mysql_engine.get_connection()
        self.df = df
        self.filename = table_name

    def run(self):
        self.df.to_sql(con=self.db_connection, name=self.filename, if_exists="append")
        self.db_connection.dispose()


def write_to_db(df: DataFrame, table_name: str, threads_num: int):
    if df.empty:
        print("Dataframe can not be empty")
        return

    threads = []
    total = len(df)
    batch_size = int(total / threads_num)
    print("Start multi threads writing, batch size is " + str(batch_size))

    for i in range(0, threads_num + 1):
        batch = df.iloc[i * batch_size:min(i * batch_size + batch_size, total)]
        print("writing batch " + str(i))
        thread = DatabaseIO(batch, table_name, i)
        threads.append(thread)
        thread.start()
        if i == 0:
            thread.join()

    for t in threads:
        t.join()

    print("All treads finished!")

def read_from_db(table_name: str = None, sql: str = None):
    if table_name is not None:
        pickle_path = FILEPATH.BASE_PATH + "/data/pickles/" + table_name
        try:
            return pd.read_pickle(pickle_path)
        except FileNotFoundError:
            print("No existing pickle, will try to read from the database")

        sql = "select * from " + table_name

    print("Using sql: " + sql)
    print("Reading the database")
    connection = mysql_engine.get_connection()
    df = pd.read_sql(sql, connection)
    connection.dispose()
    print(df.head())

    if table_name is not None:
        print("Creating pickle...")
        df.to_pickle(pickle_path)
        print("Finished")
    return df
