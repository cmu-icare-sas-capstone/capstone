import sqlalchemy
from .DBConfiguration import Configuration


class MySQLEngine:
    def __init__(self):
        self.database_username = Configuration.username
        self.database_password = Configuration.password
        self.database_ip = Configuration.host
        self.database_name = Configuration.database

    def get_connection(self):
        return sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                       format(self.database_username, self.database_password,
                                                              self.database_ip, self.database_name))


mysql_engine = MySQLEngine()
