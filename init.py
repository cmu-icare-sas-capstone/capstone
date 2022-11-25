from bean.GlobalState import get_global_state
from bean.logger import get_logger
from DatabaseConnection import DatabaseConnection
from repository.Repository import Repository
from service.DefaultProcessService import DefaultProcessService
import configuration.AppConfiguration as app_config
import pandas as pd

state = get_global_state()

logger = get_logger(__name__)

logger.debug("creating connection of database")
db_conn = DatabaseConnection(app_config=app_config).get_connection()
logger.debug("adding database connection to global")
db_conn = state.get_or_default("db_conn", db_conn)

logger.debug("creating repository")
repo = Repository(app_config=app_config, conn=db_conn)
repo = state.get_or_default("repo", repo)

logger.debug("adding default processing service")
default_process_service = DefaultProcessService(repo)
default_process_service = state.get_or_default("default_process_service", default=default_process_service)

if app_config.env == "dev" and app_config.process_default_data:
    logger.debug("env: dev, process default data: true")
    if not repo.exists_table("default"):
        logger.debug("loading default data")
        df = pd.read_csv(app_config.default_csv_path)
        repo.save_df(df, "default_data")
        table_name = default_process_service.process("default_data")

