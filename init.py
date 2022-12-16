from bean.logger import get_logger
from bean.DatabaseConnection import DatabaseConnection
from repository.Repository import Repository
from service.DefaultProcessService import DefaultProcessService
from repository.MetaDataRepository import MetaDataRepository
import configuration.AppConfiguration as app_config
import pandas as pd
from bean.GlobalState import state
import pickle
import codecs


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
create_table = "CREATE TABLE metadata(name TEXT, values TEXT, dimensions TEXT, size BIGINT)"
repo.execute_without_result(create_table)
create_table = "CREATE TABLE view(table_name TEXT, view_name TEXT, values TEXT, rules TEXT)"
repo.execute_without_result(create_table)
create_table = "CREATE TABLE comment_table(table_name TEXT, size BIGINT, status BOOLEAN)"
repo.execute_without_result(create_table)
create_table = "CREATE TABLE pickle(name TEXT, file BLOB)"
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
            ["age_group, race, facility_id, ccs_description_description", "gender"],
            ["length_of_stay", "total_costs", "long_stay"],
            1000000
        )
        df = repo.read_df("default_data_clean")
        df.to_pickle("data7_0")


elif app_config.env == "test":
    logger.debug("env: test_, process default data: true")
    if not repo.exists_table("default_data_clean"):
        logger.debug("loading default data")
        table_name = "default_data_clean"
        df = pd.read_pickle("data/pickles/test_data")
        repo.save_df(df, "default_data_clean")
        meta_data_repo.add_meta_data(
            table_name,
            ["age_group, race, facility_id, ccs_diagnosis_description, gender"],
            ["length_of_stay", "total_costs", "long_stay"],
            1000000
        )
        df = pd.read_pickle("data/pickles/clean_test")
        repo.save_df(df, "default_data_clean_model")
    if not repo.exists_table("default_comments"):
        comments = pd.read_pickle("data/pickles/default_comments")
        comments = pd.DataFrame(comments)
        repo.save_df(comments, "default_comments")
        sql = "INSERT INTO comment_table VALUES ('%s', %s, %s)" % ("default_comments", 90000000, True)
        repo.execute(sql)

        processed_comments = pickle.load(open("./model/processed_comments.pkl", 'rb'))
        processed_comments_encoded = codecs.encode(pickle.dumps(processed_comments), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_processed_comments_", processed_comments_encoded)
        repo.execute(sql)

        processed_comments_recomm = pickle.load(open("./model/processed_comments_recom.pkl", 'rb'))
        processed_comments_recomm_encoded = codecs.encode(pickle.dumps(processed_comments_recomm), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_processed_comments_" + "recomm", processed_comments_recomm_encoded)
        repo.execute(sql)

        svdMatrix_encoded = pickle.load(open("./model/svdMatrix.pkl", 'rb'))
        svdMatrix_encoded = codecs.encode(pickle.dumps(svdMatrix_encoded), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_svdMatrix_", svdMatrix_encoded)
        repo.execute_without_result(sql)

        svdMatrix_encoded = pickle.load(open("./model/svdMatrix_recom.pkl", 'rb'))
        svdMatrix_encoded = codecs.encode(pickle.dumps(svdMatrix_encoded), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_svdMatrix_recomm", svdMatrix_encoded)
        repo.execute_without_result(sql)

        tsne_lsa_vectors_encoded = pickle.load(open("./model/tsne_lsa_vectors.pkl", 'rb'))
        tsne_lsa_vectors_encoded = codecs.encode(pickle.dumps(tsne_lsa_vectors_encoded), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_tsne_lsa_vectors_", tsne_lsa_vectors_encoded)
        repo.execute_without_result(sql)

        tsne_lsa_vectors_encoded = pickle.load(open("./model/tsne_lsa_vectors_recom.pkl", 'rb'))
        tsne_lsa_vectors_encoded = codecs.encode(pickle.dumps(tsne_lsa_vectors_encoded), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_tsne_lsa_vectors_recomm", tsne_lsa_vectors_encoded)
        repo.execute_without_result(sql)

        keywords_comments = pickle.load(open("./model/keywords_comments.pkl", 'rb'))
        keywords_comments = codecs.encode(pickle.dumps(keywords_comments), "base64").decode()
        sql = "INSERT INTO pickle VALUES ('%s', '%s')" % ("default_comments" + "_keywords_comments", keywords_comments)
        repo.execute_without_result(sql)
