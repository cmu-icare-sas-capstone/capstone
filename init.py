from bean.logger import get_logger
from bean.DatabaseConnection import DatabaseConnection
from repository.Repository import Repository
from service.DefaultProcessService import DefaultProcessService
from repository.MetaDataRepository import MetaDataRepository
import configuration.AppConfiguration as app_config
import pandas as pd
from bean.GlobalState import state


logger = get_logger(__name__)

logger.debug("creating connection of database")
db_conn = DatabaseConnection(app_config=app_config).get_connection()
logger.debug("adding database connection to global")
db_conn = state.get_or_default("db_conn", db_conn)

logger.debug("creating repository")
repo = Repository(app_config=app_config, conn=db_conn)
repo = state.get_or_default("repo", repo)
meta_data_repo = MetaDataRepository(repo)
meta_data_repo = state.get_or_default("meta_data_repo", meta_data_repo)
logger.debug(meta_data_repo)
logger.debug(state.get("meta_data_repo"))

# add meta data repo
create_table = "CREATE TABLE metadata(name TEXT, values TEXT, dimensions TEXT)"
repo.execute_without_result(create_table)
create_table = "CREATE TABLE view(table_name TEXT, view_name TEXT, values TEXT, rules TEXT)"
repo.execute_without_result(create_table)

logger.debug("adding default processing service")
default_process_service = DefaultProcessService(repo)
default_process_service = state.get_or_default("default_process_service", default=default_process_service)

if app_config.env == "dev" and app_config.process_default_data:
    logger.debug("env: dev, process default data: true")
    if not repo.exists_table("default_data_clean"):
        logger.debug("loading default data")
        table_name = "default_data"
        df = pd.read_csv("data/files/hospital_episodes_inpatient_discharges_7_0.csv")
        repo.save_df(df, "default_data")
        default_process_service.process("default_data")
        meta_data_repo.add_meta_data(
            table_name+"_clean",
            ["age_group, race, facility_id, ccs_description_description"],
            ["length_of_stay", "total_costs", "long_stay"]
        )
        df = repo.read_df("default_data_clean")
        df.to_pickle("data7_0")


elif app_config.env == "test":
    logger.debug("env: test, process default data: true")
    if not repo.exists_table("default_data_clean"):
        logger.debug("loading default data")
        table_name = "default_data_clean"
        df = pd.read_pickle("./data/pickles/test_data")
        repo.save_df(df, "default_data_clean")
        meta_data_repo.add_meta_data(
            table_name,
            ["age_group, race, facility_id, ccs_description_description"],
            ["length_of_stay", "total_costs", "long_stay"]
        )