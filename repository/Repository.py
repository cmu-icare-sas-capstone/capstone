import repository.DuckRepository as duck
from pandas import DataFrame
from bean.Beans import logger
from repository.GlobalState import get_global_state


class Repository:
    def __init__(self):
        self.repo = duck.repo

    def execute(self, sql):
        return self.repo.execute(sql)

    def execute_without_result(self, sql):
        return self.repo.execute_without_result(sql)

    def save_df(self, df: DataFrame, name: str):
        logger.debug("save df " + name)
        self.repo.save_df(df, name)

    def read_df(self, name):
        return self.repo.read_df(name)

    def get_datatype(self, data_type: str):
        return self.repo.get_datatype(data_type)

    def exists_table(self, table_name: str):
        return self.repo.exists_table(table_name)

    def get_all_views(self):
        return self.repo.get_all_views()


global_state = get_global_state()

if global_state.get("repo") is None:
    repo = Repository()
    global_state.put("repo", repo)

repo = global_state.get("repo")
