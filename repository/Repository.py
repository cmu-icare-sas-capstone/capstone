from pandas import DataFrame
from bean.logger import get_logger
from repository.DuckRepository import DuckRepository


logger = get_logger(__name__)


class Repository:
    def __init__(self, app_config, conn):
        if app_config.env == "dev" \
                or app_config.env == "test"\
                or app_config.env == "prod":
            self.repo = DuckRepository(conn)

    def execute(self, sql):
        return self.repo.execute(sql)

    def execute_without_result(self, sql):
        return self.repo.execute_without_result(sql)

    def save_df(self, df: DataFrame, name: str):
        self.repo.save_df(df, name)

    def read_df(self, name):
        return self.repo.read_df(name)

    def get_datatype(self, data_type: str):
        return self.repo.get_datatype(data_type)

    def exists_table(self, table_name: str):
        return self.repo.exists_table(table_name)

    def get_all_views(self):
        return self.repo.get_all_views()

    def peak_table(self, table_name):
        return self.repo.peak_table(table_name)

    def delete_table(self, table_name):
        self.repo.delete_table(table_name)

    def remove_df(self, name):
        self.delete_table(name)

    def get_values_of_one_column(self, table_name, column):
        return self.repo.get_values_of_one_column(table_name, column)

    def get_values_of_one_column_by_filters(self, table_name, column, filters):
        return self.repo.get_values_of_one_column_by_filters(table_name, column, filters)

    def get_values_of_one_column_by_query(self, query):
        return self.repo.get_values_of_one_column_by_query(query)