from bean.logger import get_logger

logger = get_logger(__name__)


class MetaDataRepository:
    def __init__(self, repo):
        self.repo = repo

    def get_table_columns(self, table_name: str):
        df = self.repo.execute("SELECT * FROM %s LIMIT 5" % table_name)
        return df.columns

    def add_meta_data(self, table_name, dimensions, values):
        sql = "INSERT INTO %s VALUES ('%s', '%s', '%s')" \
              % ("metadata", table_name, ",".join(values), ",".join(dimensions))
        logger.debug(sql)
        self.repo.execute_without_result(sql)

    def get_all_tables(self):
        sql = "SELECT name FROM %s" % "metadata"
        tables = self.repo.execute_without_result(sql).fetchall()
        table_list = []
        for t in tables:
            table_list.append(t[0])
        return table_list

    def get_dimensions(self, table_name: str) -> list:
        sql = "SELECT dimensions from metadata WHERE name = '%s'" % table_name
        logger.debug(sql)
        dimensions = self.repo.execute_without_result(sql).fetchone()[0].split(",")
        dimensions = [i.strip() for i in dimensions]
        return dimensions

    def get_values(self, table_name: str) -> list:
        sql = "SELECT values from metadata WHERE name = '%s'" % table_name
        logger.debug(sql)
        return self.repo.execute_without_result(sql).fetchone()[0].split(",")

    def get_dataset_column_values(self, table_name, column) -> list:
        sql = "SELECT DISTINCT %s FROM %s ORDER BY 1" % (column, table_name)
        logger.debug(sql)
        l = []
        for x in self.repo.execute_without_result(sql).fetchall():
            l.append(x[0])
        return l

    def get_views(self, table_name):
        sql = "SELECT view_name FROM view WHERE table_name = '%s'" % table_name
        logger.debug(sql)
        res = self.repo.execute_without_result(sql).fetchall()
        view_list = []
        for r in res:
            view_list.append(r[0])
        return view_list

    def exists_view(self, view_name, dataset_name):
        sql = "SELECT EXISTS (SELECT view_name FROM view WHERE view_name = '%s' AND table_name = '%s')"\
              % (view_name, dataset_name)
        logger.debug(sql)
        res = self.repo.execute_without_result(sql).fetchone()
        return bool(res[0])

