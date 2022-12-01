from configuration.DuckDbConfiguration import duckdb_configuration


class DatabaseConnection:
    def __init__(self, app_config):
        if app_config.env == "dev":
            self.conn = duckdb_configuration.get_connection()
        if app_config.env == "test":
            self.conn = duckdb_configuration.get_connection()
        if app_config.env == "prod":
            self.conn = duckdb_configuration.get_connection()

    def get_connection(self):
        return self.conn
