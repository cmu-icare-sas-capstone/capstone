from bean.logger import get_logger
from bean.GlobalState import state

"""
rules: {
    filters: {
        "column_name": []
    }
    values: []
}
"""

logger = get_logger(__name__)
meta_data_repo = state.get("meta_data_repo")
repo = state.get("repo")


class Cube:
    def __init__(self, dataset_name: str, cube_name: str, values: list = [], rules={}):
        self.dataset_name = dataset_name
        self.cube_name = cube_name
        self.values = values
        self.dimensions = meta_data_repo.get_dimensions(dataset_name)
        self.rules = rules

    def persist_cube(self, rules):
        self.rules = rules
        sql = "CREATE OR REPLACE View %s AS %s" % (self.cube_name, self.parse_sql_from_rules(rules))
        logger.debug(sql)
        repo.execute_without_result(sql)
        sql = "UPDATE \"view\" SET values = '%s' WHERE table_name='%s' AND view_name='%s'" \
              % (",".join(self.values), self.dataset_name, self.cube_name)
        logger.debug(sql)
        repo.execute_without_result(sql)
        sql = "UPDATE \"view\" SET rules = '%s' WHERE table_name='%s' AND view_name='%s'" \
              % (str(self.rules).replace("'", ""), self.dataset_name, self.cube_name)
        logger.debug(sql)
        repo.execute_without_result(sql)

    def counts(self):
        sql = "SELECT COUNT(*) FROM %s" % self.cube_name
        logger.debug(sql)
        count = repo.execute_without_result(sql).fetchone()
        return count[0]

    def get_values(self):
        sql = "SELECT %s FROM %s" % (",".join(self.values), self.cube_name)
        logger.debug(sql)
        return repo.execute(sql)

    def parse_sql_from_rules(self, rules):
        if len(rules["filters"]) == 0:
            sql = "SELECT * FROM %s" % self.dataset_name
            return sql

        sql = "SELECT * FROM %s WHERE " % self.dataset_name
        for col in rules["filters"].keys():
            l = [str(x) for x in rules["filters"][col]]
            sub_sql = "%s in (%s)" % (col, "'" + ("','".join(l)) + "'")
            sql = sql + sub_sql + " AND "
        sql = sql[0: -5]
        logger.debug(sql)
        return sql

    def peek_cube(self, rules):
        self.values = rules["values"]
        sql = "SELECT %s FROM (%s)" % (",".join(self.values), self.parse_sql_from_rules(rules))
        logger.debug(sql)
        return repo.execute(sql)

    # same as whole data
    def init_cube(self):
        sql = "CREATE VIEW %s AS SELECT * FROM %s" % (self.cube_name, self.dataset_name)
        repo.execute_without_result(sql)
        sql = "INSERT INTO \"view\" VALUES ('%s', '%s', '%s', '%s')" \
              % (self.dataset_name, self.cube_name, ",".join(self.values), str(self.rules))
        repo.execute_without_result(sql)

    @property
    def cube_data(self):
        df = repo.execute("SELECT * FROM %s" % self.cube_name)
        logger.debug(df.head())
        return df

    def get_group_by_values(self, group_by: list, value: list, calc: list):
        cols = [x for x in group_by]
        for x in value:
            for c in calc:
                cols.append("%s(%s) as %s_%s" % (c, x, c, x))

        sql = "SELECT %s FROM %s GROUP BY %s" % (",".join(cols), self.cube_name, ",".join(group_by))
        logger.debug(sql)
        return repo.execute(sql)

    @staticmethod
    def get_cube(dataset_name, cube_name):
        sql = "SELECT values, rules from \"view\" WHERE table_name='%s' and view_name='%s'" % (dataset_name, cube_name)
        res = repo.execute_without_result(sql).fetchone()
        values = res[0]
        if len(values) > 0:
            values = values.split(",")
        else:
            values = []
        rules = res[1]
        logger.debug(rules)
        cube = Cube(dataset_name, cube_name, values, rules)
        return cube
