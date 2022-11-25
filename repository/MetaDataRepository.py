from repository.Repository import repo
from bean.Beans import logger


class MetaDataRepository:
    def __init__(self):
        self.repo = repo

    def get_table_columns(self, table_name: str):
        df = self.repo.execute("SELECT * FROM %s LIMIT 5" % table_name)
        return df.columns

    def add_meta_data(self, table_name, dimensions, values):
        sql = "INSERT INTO %s VALUES ('%s', '%s', '%s')" \
              % ("metadata", table_name,",".join(values), ",".join(dimensions))
        logger.debug(sql)
        repo.execute_without_result(sql)

    def get_all_table_names(self):
        sql = "SELECT name FROM %s" % "metadata"
        return repo.execute_without_result(sql).fetchone()

    def get_dimensions(self, table_name: str) -> list:
        sql = "SELECT dimensions from metadata WHERE name = '%s'" % table_name
        return repo.execute_without_result(sql).fetchone()[0].split(",")

    def get_values(self, table_name: str) -> list:
        sql = "SELECT values from metadata WHERE name = '%s'" % table_name
        return repo.execute_without_result(sql).fetchone()[0].split(",")

    def get_dataset_column_values(self, table_name, column):
        sql = "SELECT DISTINCT %s FROM %s ORDER BY 1" % (column, table_name)
        l = []
        for x in repo.execute_without_result(sql).fetchall():
            l.append(x[0])
        return l


meta_data_repo = MetaDataRepository()
