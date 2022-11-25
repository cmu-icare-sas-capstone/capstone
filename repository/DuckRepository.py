from configuration.DuckDbConfiguration import duckdb_configuration
from pandas import DataFrame
from bean.Beans import logger


class DuckRepository:
    data_types = {
        "int": "INTEGER",
        "float": "REAL",
        "object": "TEXT",
        "str": "TEXT"
    }

    def __init__(self):
        self.conn = duckdb_configuration.get_connection()

    def execute(self, sql):
        return self.conn.execute(query=sql).df()

    def execute_without_result(self, sql):
        return self.conn.execute(query=sql)

    def save_df(self, df: DataFrame, name: str):
        df.columns = df.columns.str.lower()
        df = df.loc[:, ~df.columns.duplicated()]
        exist = self.exists_table(name)
        if exist:
            return
        self.conn.register("df", df)
        self.conn.execute("CREATE TABLE %s AS SELECT * FROM df" % name)
        self.conn.unregister("df")

    def read_df(self, name):
        sql = "SELECT * FROM " + name
        return self.execute(sql)

    def get_datatype(self, data_type: str):
        return self.data_types[data_type]

    def exists_table(self, table_name: str) -> bool:
        sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '%s'" % table_name
        logger.debug(sql)
        count = self.execute_without_result(sql).fetchone()[0]
        logger.debug(count)
        return count == 1

    def get_all_views(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_type = 'VIEW'"
        logger.debug(sql)
        views = self.execute_without_result(sql).fetchone()
        if views is None:
            return []
        logger.debug(type(views))
        return list(views)


repo = DuckRepository()
