import pandas as pd

from frontend.components.BubbleChart import BubbleChart
import matplotlib.pyplot as plt
import streamlit as st
import random
from wordcloud import WordCloud
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
from keybert import KeyBERT
repo = state.get("repo")


def create_nlp_page():
    show_option = st.selectbox(
        label="",
        options=("Key Phrases", "Topic Modeling On All Comments", "Topic Modeling On Recommendations", "KeyBert")
    )

    keywords = [('services', 33062), ('cms', 28732), ('patients', 22148), ('health', 19614), ('care', 18837),
                ('medicare', 17899), ('access', 16054), ('cuts', 15917), ('management', 15208), ('therapy', 13823),
                ('codes', 13292), ('proposed', 12376), ('psychologists', 10412), ('reimbursement', 9869),
                ('patient', 9028), ('behavioral', 8573), ('supervision', 8560), ('training', 8245), ('support', 8071),
                ('treatment', 7927)]

    key_phrases = [('psychological services medicare', 0.6466),
                   ('psychotherapeutic services medicare', 0.637),
                   ('services cms medicare', 0.6348),
                   ('cms proposed medicare', 0.6247),
                   ('medicare requests cms', 0.6243),
                   ('utilize cms medicare', 0.6241),
                   ('medicare cms regarding', 0.6137),
                   ('medicare program cms', 0.6135),
                   ('cms behavioral health', 0.6134),
                   ('cms strengthen medicare', 0.6116),
                   ('outpatient services cms', 0.6098),
                   ('provide behavioral healthcare', 0.6083),
                   ('cms understanding medicare', 0.6074),
                   ('behavioral healthcare services', 0.6066),
                   ('cms medicare program', 0.6066),
                   ('cms beneficiaries outpatient', 0.606),
                   ('integrated behavioral healthcare', 0.6057),
                   ('treatment cms policies', 0.6054),
                   ('medicare clients cms', 0.6049),
                   ('cms ensure medicare', 0.6036)]
    key_phrases_dict = {}
    for t in key_phrases:
        key_phrases_dict[t[0]] = t[1]

    if show_option == "Key Phrases":
        cloud = WordCloud(max_font_size=50, max_words=100, background_color="white")\
            .generate_from_frequencies(key_phrases_dict)
        fig, ax = plt.subplots()
        plt.title("All Comments - Wordcloud")
        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    elif show_option == "Topic Modeling On All Comments":
        draw_tsne_graph_on_comments()
    elif show_option == "Topic Modeling On Recommendations":
        draw_tsne_graph_on_comments("_recom")
    elif show_option == "KeyBert":
        create_keybert_table()


def draw_tsne_graph_on_comments(comments_set=""):
    import pickle

    with open("./model/processed_comments" + comments_set + ".pkl", 'rb') as file:
        processed_comments = pickle.load(file)

    tf_vectorizer = CountVectorizer()
    tf_vectorizer.fit(processed_comments)

    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(processed_comments)

    n_topics = 8

    import pickle

    with open("./model/svdMatrix" + comments_set + ".pkl", 'rb') as file:
        svdMatrix = pickle.load(file)

    with open("./model/tsne_lsa_vectors" + comments_set + ".pkl", "rb") as file:
        tsne_lsa_vectors = pickle.load(file)

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

def create_keybert_table():
    import pickle
    with open("./model/keywords_comments.pkl", 'rb') as file:
        processed_comments = pickle.load(file)

    df = pd.DataFrame(data=processed_comments, columns=["Keyword", "Weight"])
    st.table(df)
