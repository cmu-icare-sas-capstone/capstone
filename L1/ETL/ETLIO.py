import threading

import pandas
from Utils.MySQLEngine import mysql_engine
from pandas import DataFrame


class ETLIO(threading.Thread):
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
    threads = []
    total = len(df)
    batch_size = int(total / threads_num)
    print("Start multi threads writing, batch size is " + str(batch_size))

    for i in range(0, threads_num + 1):
        batch = df.iloc[i*batch_size:min(i*batch_size + batch_size, total)]
        print("writing batch " + str(i))
        thread = ETLIO(batch, table_name, i)
        threads.append(thread)
        thread.start()
        if i == 0:
            thread.join()

    for t in threads:
        t.join()

    print("All treads finished!")


# TODO: if local pickle exists, read from local
def read_from_db(table_name: str):
    sql = "select * from " + table_name
    return pandas.read_sql(sql, mysql_engine.get_connection())
