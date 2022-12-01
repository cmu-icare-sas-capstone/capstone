from bean.logger import get_logger
import configuration.AppConfiguration as app_config
logger = get_logger(__name__)


def test():
    app_config.env = "test"
    from bean.GlobalState import state
    import init
    repo = state.get("repo")
    meta_data_repo = state.get("meta_data_repo")
    test_add_exists_view(repo, meta_data_repo)


def test_add_exists_view(repo, meta_data_repo):
    sql = "INSERT INTO view VALUES ('default_data_clean', 'test', 'total_costs, length_of_stay', '{}')"
    logger.debug(sql)
    repo.execute_without_result(sql)
    sql = "CREATE VIEW test AS SELECT * FROM default_data_clean"
    repo.execute_without_result(sql)
    flag = meta_data_repo.exists_view("test", "default_data_clean")
    print(flag)


test()
