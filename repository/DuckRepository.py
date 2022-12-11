from pandas import DataFrame
from bean.logger import get_logger


logger = get_logger(__name__)


class DuckRepository:
    data_types = {
        "int": "INTEGER",
        "float": "REAL",
        "object": "TEXT",
        "str": "TEXT"
    }

    def __init__(self, conn):
        self.conn = conn

    def execute(self, sql) -> DataFrame:
        return self.conn.execute(query=sql).df()

    def execute_without_result(self, sql):
        return self.conn.execute(query=sql)

    def save_df(self, df: DataFrame, name: str):
        df.columns = df.columns.str.lower()
        df = df.loc[:, ~df.columns.duplicated()]
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
        views = self.execute_without_result(sql).fetchall()
        view_list = []
        for v in views:
            view_list.append(v[0])
        return view_list

    def peak_table(self, table_name) -> DataFrame:
        sql = "SELECT * FROM \"%s\" LIMIT 20" % table_name
        logger.debug(sql)
        return self.execute(sql)

    def delete_table(self, table_name) -> DataFrame:
        sql = "DROP TABLE IF EXISTS \"%s\"" % table_name
        logger.debug(sql)
        self.execute_without_result(sql)

    def get_values_of_one_column(self, table_name, column):
        sql = "SELECT DISTINCT %s FROM %s" % (column, table_name)
        logger.debug(sql)
        values = self.execute_without_result(sql).fetchall()
        value_list = []
        for v in values:
            value_list.append(v[0])
        value_list.sort()
        return value_list

    def get_values_of_one_column_by_query(self, query):
        values = self.execute_without_result(query).fetchall()
        value_list = []
        for v in values:
            value_list.append(v[0])
        value_list.sort()
        return value_list

    def get_values_of_one_column_by_filters(self, table_name, column, filters):
        sql = "SELECT DISTINCT %s FROM %s WHERE " % (column, table_name)
        for key in filters:
            sql = sql + "%s in (%s)" % (key, ("'" + "','".join(filters[key]) + "'"))
        logger.debug(sql)
        values = self.execute_without_result(sql).fetchall()
        value_list = []
        for v in values:
            value_list.append(v[0])
        value_list.sort()
        return value_list

    def alter_table_name(self, oldname, newname):
        sql = "ALTER TABLE %s RENAME to %s" % (oldname, newname)
        self.execute_without_result(sql)