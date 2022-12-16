import pickle

import pandas as pd

import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from bean.GlobalState import state
import numpy as np
from collections import Counter
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label
from bokeh.io import output_notebook
output_notebook()
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import spacy
from spacy.tokens import Doc
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import string
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
import codecs
from sklearn.manifold import TSNE
import re
from keybert import KeyBERT


repo = state.get("repo")


def create_nlp_page():
    sql = "SELECT table_name FROM comment_table"
    comment_sets = repo.execute(sql)
    comment_sets = comment_sets.iloc[:, 0].tolist()
    comment_set = st.selectbox(
        label="Comment set",
        options=comment_sets,
    )

    show_option = st.selectbox(
        label="",
        options=("Key Phrases", "Topic Modeling On All Comments", "Topic Modeling On Recommendations", "KeyBert")
    )
    df = pd.DataFrame()
    if comment_set is not None:
        df = repo.read_df(comment_set)

    st.markdown("It may take up to 15 minutes to run the NLP engine on the dataset, "
                "it need to be run on every new comments set once")
    if st.button("Run NLP Engine"):
        with st.spinner("Running NLP Engine"):
            df = df.dropna(thresh=df.shape[0] * 0.8, axis=1)  # 43 columns dropped
            df = df.dropna(how="all", axis=1)

            # drop rows where there is no comment
            df = df.dropna(subset=['comment'])

            # Delete duplicate rows based on specific columns
            df.drop_duplicates(subset=["comment"], keep='first', inplace=True)

            # tsne
            comments = df.loc[:, "comment"]
            run_nlp(comments, comment_set)

            # tsne recommend
            # Create a regular expression pattern that matches any of the specified search strings
            pattern = re.compile("urge|recommend|advise", re.IGNORECASE)
            # filter dataset to include only comments with intention of making recommendations
            recommend_df = comments[comments.str.contains(pattern)]
            run_nlp(recommend_df, comment_set, "recomm")

            sql = "UPDATE comment_table SET status = true WHERE table_name = '%s'" % comment_set
            repo.execute_without_result(sql)

    sql = "SELECT status FROM comment_table WHERE table_name = '%s'" % comment_set
    status = repo.execute_without_result(sql).fetchone()
    if status is not None:
        status = status[0]

    if status:
        if show_option == "Key Phrases":
            run_wordcloud(df)
        elif show_option == "Topic Modeling On All Comments":
            draw_tsne_graph_on_comments(comment_set=comment_set)
        elif show_option == "Topic Modeling On Recommendations":
            draw_tsne_graph_on_comments(comment_set=comment_set, postfix="recomm")
        elif show_option == "KeyBert":
            create_keybert_table(comment_set)


def draw_tsne_graph_on_comments(comment_set="", postfix=""):
    import pickle

    sql = "SELECT file FROM pickle WHERE name='%s'" % (comment_set + "_processed_comments_" + postfix)
    res = repo.execute_without_result(sql).fetchone()[0]
    processed_comments = pickle.loads(codecs.decode(res, "base64"))

    tf_vectorizer = CountVectorizer()
    tf_vectorizer.fit(processed_comments)

    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(processed_comments)

    n_topics = 8

    sql = "SELECT file FROM pickle WHERE name='%s'" % (comment_set + "_svdMatrix_" + postfix)
    res = repo.execute_without_result(sql).fetchone()[0]
    svdMatrix = pickle.loads(codecs.decode(res, "base64"))

    sql = "SELECT file FROM pickle WHERE name='%s'" % (comment_set + "_tsne_lsa_vectors_" + postfix)
    res = repo.execute_without_result(sql).fetchone()[0]
    tsne_lsa_vectors = pickle.loads(codecs.decode(res, "base64"))


    def get_keys(topic_matrix):
        '''returns an integer list of predicted topic categories for a given topic matrix'''
        keys = []
        for i in range(topic_matrix.shape[0]):
            keys.append(topic_matrix[i].argmax())
        return keys

    def keys_to_counts(keys):
        '''returns a tuple of topic categories and their accompanying magnitudes for a given list of keys'''
        count_pairs = Counter(keys).items()
        categories = [pair[0] for pair in count_pairs]
        counts = [pair[1] for pair in count_pairs]
        return (categories, counts)

    def get_mean_topic_vectors(keys, two_dim_vectors):
        '''returns a list of centroid vectors from each predicted topic category'''
        mean_topic_vectors = []
        for t in range(n_topics):
            articles_in_that_topic = []
            for i in range(len(keys)):
                if keys[i] == t:
                    articles_in_that_topic.append(two_dim_vectors[i])

            articles_in_that_topic = np.vstack(articles_in_that_topic)
            mean_article_in_that_topic = np.mean(articles_in_that_topic, axis=0)
            mean_topic_vectors.append(mean_article_in_that_topic)
        return mean_topic_vectors

    def get_top_n_words(n, keys, document_term_matrix, count_vectorizer):
        '''returns a list of n_topic strings, where each string contains the n most common
            words in a predicted category, in order'''
        top_word_indices = []
        for topic in range(n_topics):
            temp_vector_sum = 0
            for i in range(len(keys)):
                if keys[i] == topic:
                    temp_vector_sum += document_term_matrix[i]
            temp_vector_sum = temp_vector_sum.toarray()
            top_n_word_indices = np.flip(np.argsort(temp_vector_sum)[0][-n:], 0)
            top_word_indices.append(top_n_word_indices)
        top_words = []
        for topic in top_word_indices:
            topic_words = []
            for index in topic:
                temp_word_vector = np.zeros((1, document_term_matrix.shape[1]))
                temp_word_vector[:, index] = 1
                the_word = count_vectorizer.inverse_transform(temp_word_vector)[0][0]
                topic_words.append(the_word.encode('ascii').decode('utf-8'))
            top_words.append(" ".join(topic_words))
        return top_words

    color_text = [(90, 90, 90), (90, 90, 90), (90, 90, 90), (90, 90, 90), (90, 90, 90), (90, 90, 90), (90, 90, 90),
                  (90, 90, 90), (90, 90, 90), (90, 90, 90), (90, 90, 90)]
    colors2 = ["#00FFFF", "#00C957", "#8A2BE2", "#8B2323", "#CDCD00", "#458B00", "#DC143C", "#EE6AA7", "#104E8B",
               "#FFEC8B", "#FF4500"]

    # Lists which category each point is associated with
    lsa_keys = get_keys(svdMatrix)
    # color associated with each point
    lsa_colors = [colors2[key] for key in lsa_keys]
    # get category and counts of documents in each category
    lsa_categories, lsa_counts = keys_to_counts(lsa_keys)
    # top words associated with each category
    top_n_words_lsa = get_top_n_words(10, lsa_keys, dtm_tfidf, tf_vectorizer)

    topic_df = pd.DataFrame({"Topic": [i for i in range(0, 8)], "Count": lsa_counts, "Words": top_n_words_lsa})

    st.table(data=topic_df)

    # Plot Results
    # Get compreesed vectors and words associated with each topic
    top_3_words_lsa = get_top_n_words(3, lsa_keys, dtm_tfidf, tf_vectorizer)
    lsa_mean_topic_vectors = get_mean_topic_vectors(lsa_keys, tsne_lsa_vectors)

    # initialize Bokeh data structures with attributes - x, y, keys, colors
    source = ColumnDataSource(
        data=dict(x=tsne_lsa_vectors[:, 0].tolist(), y=tsne_lsa_vectors[:, 1].tolist(), desc=lsa_keys,
                  color=lsa_colors))

    h = HoverTool(tooltips=[("Topic", "@desc"), ("(x,y)", "($x, $y)")])
    # create plot
    plot = figure(
        title="Topics of CMS Public Comments".format(n_topics),
        plot_width=1000, plot_height=600, tools=["pan,wheel_zoom,box_zoom,reset", h],
        toolbar_location="below", x_axis_label=' Reduced Dimension 1', y_axis_label='Reduced Dimension 2')
    # input points
    plot.scatter(x='x', y='y', source=source, color='color')

    for t in range(n_topics):
        label = Label(x=lsa_mean_topic_vectors[t][0], y=lsa_mean_topic_vectors[t][1],
                      text=top_3_words_lsa[t], text_color=color_text[t], render_mode='css',
                      text_font_size='14pt', text_font_style='bold', x_offset=0, y_offset=0)
        plot.add_layout(label)

    plot.xaxis.axis_label_text_font_size = "18pt"
    plot.yaxis.axis_label_text_font_size = "18pt"
    plot.title.text_font_size = "21pt"
    plot.title_location = "above"
    show(plot)

    st.bokeh_chart(figure=plot)

# Title: Topics of public comments (Recommendation)


def create_keybert_table(comment_set):
    import pickle

    sql = "SELECT file FROM pickle WHERE name='%s'" % (comment_set + "_keywords_comments")
    res = repo.execute_without_result(sql).fetchone()[0]
    keywords_comments = pickle.loads(codecs.decode(res, "base64"))

    df = pd.DataFrame(data=keywords_comments, columns=["Keyword", "Weight"])
    st.table(df)


def run_wordcloud(df):
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords=stop_words,
                          collocation_threshold=3).generate(str(df))
    fig, ax = plt.subplots()
    plt.title("All Comments - Wordcloud")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def run_nlp(comments, comment_set, postfix=""):
    print(comments)
    processed_comments = process_comments(comments)
    processed_comments_encoded = codecs.encode(pickle.dumps(processed_comments), "base64").decode()

    sql = "INSERT INTO pickle VALUES ('%s', '%s')" % (comment_set+"_processed_comments_"+postfix, processed_comments_encoded)

    repo.execute_without_result(sql)

    tf_vectorizer = CountVectorizer()
    tf_vectorizer.fit(processed_comments)
    dtm_tf = tf_vectorizer.transform(processed_comments)

    # term-frequency inverse document frequency (TF-IDF) matrix
    # TF-IDF is better at identifying words that are more indicative of the content of a particular comment
    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(processed_comments)

    n_topics = 8
    # Singular Value Decomposition
    svd = TruncatedSVD(n_components=n_topics)
    svdMatrix = svd.fit_transform(dtm_tfidf)
    svdMatrix = Normalizer(copy=False).fit_transform(svdMatrix)
    svdMatrix_encoded = codecs.encode(pickle.dumps(svdMatrix), "base64").decode()
    sql = "INSERT INTO pickle VALUES ('%s', '%s')" % (comment_set + "_svdMatrix_" + postfix, svdMatrix_encoded)
    repo.execute_without_result(sql)

    # Initialize TSNE
    tsne_lsa_model = TSNE(n_components=2, perplexity=50, learning_rate=100,
                          n_iter=2000, verbose=False, random_state=3, angle=0.75)
    tsne_lsa_vectors = tsne_lsa_model.fit_transform(svdMatrix)
    tsne_lsa_vectors_encoded = codecs.encode(pickle.dumps(tsne_lsa_vectors), "base64").decode()
    sql = "INSERT INTO pickle VALUES ('%s', '%s')" % (comment_set + "_tsne_lsa_vectors_" + postfix, tsne_lsa_vectors_encoded)
    repo.execute_without_result(sql)

    extract_keywords(comments, comment_set)
    return


def process_comments(df):
    '''
    Process the comments from the given dataframe
    '''
    comments = df.to_numpy() # extract all comments into an array
    tknzr = TweetTokenizer()
    nlp = spacy.load("en_core_web_sm") # NLP for english
    lemmatizer = WordNetLemmatizer()

    # customized a class for tweet tokenizer
    def tweet_tokenize(x):
        return Doc(nlp.vocab, words = tknzr.tokenize(x))

    # set our nlp pipeline with tokenizer specialized for tweets
    nlp.tokenizer = tweet_tokenize

    processed_comments = []
    remove_words = ['<br/>']

    # loop over each comment
    for comment in comments:

        processed_comment = []

        # Convert comment into Doc object with a sequence of tokens
        for token in nlp(str(comment).lower()):
            if token.text in nlp.Defaults.stop_words or 'http' in token.text or token.text in string.punctuation or len(token.text) < 2 or token.text in remove_words: # remove stop words
                continue
            else:
                processed_comment.append(lemmatizer.lemmatize(token.text))

        processed_comments.append(' '.join(processed_comment))

    return processed_comments

def extract_keywords(df, comment_set):
   '''
   Extract keywords based on KeyBERT from the provided dataframe
   '''
   kw_model = KeyBERT()
   # Extract keywords from all comments
   all_comments = ""
   for i in range(0, len(df)):
      all_comments  = all_comments  + " " + str(df.iloc[i])

   keywords_comments = kw_model.extract_keywords(all_comments,keyphrase_ngram_range=(1, 2), stop_words=None)
   keywords_comments_encoded = codecs.encode(pickle.dumps(keywords_comments), "base64").decode()
   sql = "INSERT INTO pickle VALUES ('%s', '%s')" % (comment_set + "_keywords_comments", keywords_comments_encoded)
   repo.execute_without_result(sql)
   return