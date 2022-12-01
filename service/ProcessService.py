import re
from bean.logger import get_logger
'''
clean rules: {
    columns: []

    rename: {
        column_name: "newName"
    },

    retype: {
        column_name: "newType"
    },
    
    filters: {
        columns_name: []
    }
}
'''

logger = get_logger(__name__)


class ProcessService:
    special_chars_values = r"(\s|:|\(|\)|\-|\+|\$|>)"
    special_chars_col_name = r"(\s|:|\(|\)|\-|\+|\$|>|\.)"

    def __init__(self, repo):
        self.repo = repo

    def clean(self, df_name: str, rules: dict):
        logger.debug("cleaning the dataset by rules %s", str(rules))
        cleaned_table = df_name + "_clean"

        # select columns
        sql = "CREATE TABLE \"%s\" AS SELECT %s FROM \"%s\"" \
              % (cleaned_table, "\""+("\", \"".join(rules["columns"])+"\""), df_name)
        logger.debug(sql)
        self.repo.execute_without_result(sql)

        # retype
        for col in rules["retype"]:
            sql = "UPDATE \"%s\" SET \"%s\"=%s" \
                  % (cleaned_table, col, "regexp_replace(\"%s\", %s, %s, 'g')" \
                     % (col, "'(\s|:|\(|\)|\-|\+|\$|>)'", "''"))
            logger.debug(sql)
            self.repo.execute_without_result(sql)

            sql = "ALTER TABLE \"%s\" ALTER \"%s\" TYPE %s"\
                  % (cleaned_table, col, self.repo.get_datatype(rules["retype"][col]))
            logger.debug(sql)
            self.repo.execute_without_result(sql)

        # filters
        for col in rules["filters"].keys():
            sql = "DELETE FROM \"%s\" WHERE \"%s\" NOT IN (%s)" \
                  % (cleaned_table, col, "'" + ("', '".join(rules["filters"][col]))+"'")
            logger.debug(sql)
            self.repo.execute_without_result(sql)

        for col in rules["revert_filters"].keys():
            sql = "DELETE FROM \"%s\" WHERE \"%s\" IN (%s)" \
                  % (cleaned_table, col, "'" + ("', '".join(rules["revert_filters"][col])) + "'")
            logger.debug(sql)
            self.repo.execute_without_result(sql)
        #
        for col in rules["drop_null"]:
            sql = "DELETE FROM \"%s\" WHERE \"%s\"=null" \
                  % (cleaned_table, col)
            logger.debug(sql)
            self.repo.execute_without_result(sql)
        #
        # rename
        for col in rules["rename"].keys():
            sql = "ALTER TABLE \"%s\" RENAME \"%s\" to \"%s\""\
                  % (cleaned_table, col, self.format_column_name(rules["rename"][col]))
            logger.debug(sql)
            self.repo.execute_without_result(sql)

        sql = "SELECT * FROM %s LIMIT 5" % cleaned_table
        logger.debug(sql)
        temp_df = self.repo.execute(sql)

        for col in temp_df.columns:
            sql = "ALTER TABLE \"%s\" RENAME \"%s\" to \"%s\""\
                  % (cleaned_table, col, self.format_column_name(col))

            self.repo.execute_without_result(sql)

    def feature_eng(self, df_name: str, rules: dict):
        logger.debug("feature engineering the dataset by rules %s", str(rules))
        calculations = rules["calc_columns"]
        for d in calculations:
            sql = "ALTER TABLE %s ADD COLUMN %s %s" % (df_name, d["calc_col"], self.repo.get_datatype(d["dtype"]))
            logger.debug(sql)
            self.repo.execute_without_result(sql)

            condition = ""
            for con in d["conditions"]:
                if con[0] == "gt":
                    condition += ("WHEN %s > %s THEN %s " % (d["col"], con[1], con[2]))
                elif con[0] == "set":
                    condition += ("WHEN %s <= %s THEN %s " % (d["col"], con[1], con[2]))

            sql = "UPDATE %s SET %s=(CASE %s END)" % (df_name, d["calc_col"], condition)
            logger.debug(sql)
            self.repo.execute_without_result(sql)

    def format_column_name(self, name: str) -> str:
        snake_column = name.lower().strip()
        snake_column = re.sub(self.special_chars_col_name, "_", snake_column)
        snake_column = re.sub(r"(_)\1+", "_", snake_column)
        return snake_column
