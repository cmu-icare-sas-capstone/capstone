from repository.Repository import repo
from bean.Beans import logger
from repository.MetaDataRepository import meta_data_repo
"""
rules: {
    filters: {
        "column_name": []
    }
    values: []
}
"""


class Cube:
    def __init__(self, dataset_name: str, cube_name: str):
        self.dataset_name = dataset_name
        self.cube_name = cube_name
        self.values = meta_data_repo.get_values(dataset_name)
        self.dimensions = meta_data_repo.get_dimensions(dataset_name)

    def init_cube(self, rules):
        sql = "CREATE View %s AS %s" % (self.cube_name, self.parse_sql_from_rules(rules))
        repo.execute_without_result(sql)

    def counts(self):
        sql = "SELECT COUNT(*) FROM %s" % self.cube_name
        count = repo.execute_without_result(sql).fetchone()
        return count[0]

    def get_values(self):
        sql = "SELECT %s FROM %s" % (",".join(self.values), self.cube_name)
        logger.debug(sql)
        return repo.execute(sql)

    def parse_sql_from_rules(self, rules):
        sql = "SELECT * FROM %s WHERE " % self.dataset_name
        for col in rules["filters"].keys():
            l = [str(x) for x in rules["filters"][col]]
            sub_sql = "%s in (%s)" % (col, "'" + ("','".join(l)) + "'")
            sql = sql + sub_sql + " AND "
        sql = sql[0: -5]
        logger.debug(sql)
        return sql

    def peek_cube(self, rules):
        sql = "SELECT %s FROM (%s)" % (",".join(self.values), self.parse_sql_from_rules(rules))
        return repo.execute(sql)

    @property
    def cube_data(self):
        return repo.execute("SELECT * FROM %s" % self.cube_name)

    def get_group_by_values(self, group_by: list, value: list, calc: list):
        cols = [x for x in group_by]
        for x in value:
            for c in calc:
                cols.append("%s(%s) as %s_%s" % (c, x, c, x))

        sql = "SELECT %s FROM %s GROUP BY %s" % (",".join(cols), self.cube_name, ",".join(group_by))
        logger.debug(sql)
        return repo.execute(sql)
