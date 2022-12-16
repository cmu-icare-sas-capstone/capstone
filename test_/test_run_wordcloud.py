import frontend.pages.nlp_page as nlp_page
import pandas as pd
from bean.GlobalState import state
import pickle
import codecs

repo = state.get("repo")


def test_run_wordcloud():
    comments = set_up()
    nlp_page.run_wordcloud(comments)


def test_run_nlp():
    comments = set_up()
    nlp_page.run_nlp(comments, "test")
    sql = "SELECT file FROM pickle WHERE name='%s'" % "test_processed_comments_"
    res = repo.execute_without_result(sql).fetchone()[0]
    processed_comments = pickle.loads(codecs.decode(res, "base64"))
    print(processed_comments)


def set_up():
    df = pd.read_csv("data/files/CMS_PUBLIC_COMMENTS_2022_7-9.csv")
    df = df.dropna(thresh=df.shape[0] * 0.8, axis=1)  # 43 columns dropped
    df = df.dropna(how="all", axis=1)

    # drop rows where there is no comment
    df = df.dropna(subset=['Comment'])

    # Delete duplicate rows based on specific columns
    df.drop_duplicates(subset=["Comment"], keep='first', inplace=True)
    comments = df.loc[:, ["Comment"]]
    comments = comments.rename({"Comment": "comment"})
    print(type(comments))
    repo.save_df(comments, "test")
    return comments


# test_run_wordcloud()
# test_run_nlp()