import pandas as pd
import spacy #natural language processing
from spacy.tokens import Doc
import en_core_web_sm
import pandas as pd
import csv
import codecs
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from collections import Counter
nltk.download('wordnet')
nltk.download('omw-1.4')
import string


df = pd.read_csv("data/files/CMS_PUBLIC_COMMENTS_2022_7-9.csv")

df = df.dropna(thresh=df.shape[0]*0.8,axis=1) # 43 columns dropped
df = df.dropna(how='all',axis=1)
# drop rows where there is no comment
df = df.dropna(subset=['Comment'])
df.drop_duplicates(subset=["Comment"], keep='first', inplace=True)
print('after preprocessing data...')
print(df.shape) # 13358 duplicate rows are dropped
comments = df['Comment'].to_numpy()  # extract all comments into an array

tknzr = TweetTokenizer()
nlp = spacy.load("en_core_web_sm")  # NLP for english
lemmatizer = WordNetLemmatizer()

# customized a class for tweet tokenizer
def tweet_tokenize(x):
    return Doc(nlp.vocab, words=tknzr.tokenize(x))

# set our nlp pipeline with tokenizer specialized for tweets
nlp.tokenizer = tweet_tokenize

processed_comments = []

# count top words in different categories
all_counter = Counter()
adj_counter = Counter()
noun_counter = Counter()
verb_counter = Counter()

useful_words = []
adjs = []
nouns = []
verbs = []

remove_words = ['<br/>']

entity_list = []

# loop over each comment
for comment in comments:

    processed_comment = []

    # Convert comment into Doc object with a sequence of tokens
    for token in nlp(str(comment).lower()):
        if token.text in nlp.Defaults.stop_words or 'http' in token.text or token.text in string.punctuation or len(
                token.text) < 2 or token.text in remove_words:  # remove stop words
            continue
        else:
            processed_comment.append(lemmatizer.lemmatize(token.text))

    processed_comments.append(' '.join(processed_comment))


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import OrderedDict

#build count vectorizer off of cleaned text
tf_vectorizer = CountVectorizer()
tf_vectorizer.fit(processed_comments)
dtm_tf = tf_vectorizer.transform(processed_comments)
print("shape of term frequency matrix: ", dtm_tf.shape)

tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
dtm_tfidf = tfidf_vectorizer.fit_transform(processed_comments)
print("shape of term frequency inverse document frequency matrix: ",dtm_tfidf.shape)
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
n_topics = 8
#Singular Value Decomposition
svd = TruncatedSVD(n_components = n_topics)
svdMatrix = svd.fit_transform(dtm_tfidf)
svdMatrix = Normalizer(copy=False).fit_transform(svdMatrix)
#%%time
from sklearn.manifold import TSNE

#Initialize TSNE
tsne_lsa_model = TSNE(n_components=2, perplexity=50, learning_rate=100,
                        n_iter=2000, verbose=False, random_state=3, angle=0.75)
tsne_lsa_vectors = tsne_lsa_model.fit_transform(svdMatrix)


# Define helper functions for Bokeh plotting
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

from bokeh.plotting import figure, output_file, show
from bokeh.models import Label
from bokeh.io import output_notebook
output_notebook()
from bokeh.models import HoverTool
from random import randint
from bokeh.models import ColumnDataSource

#Define colors for plotting
#colors = [(0, 220, 0), (238,203,173), (100,149,237), (69, 150, 120), (92, 60, 20), (115, 100, 50), (60, 10, 220), (255, 0, 0), (184, 140, 40), (200, 2, 109), (200, 100, 120)]
color_text = [(90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90), (90,90,90)]
colors2 = ["#00FFFF","#00C957","#8A2BE2","#8B2323","#CDCD00","#458B00","#DC143C","#EE6AA7","#104E8B","#FFEC8B","#FF4500"]

#Lists which category each point is associated with
lsa_keys = get_keys(svdMatrix)
#color associated with each point
lsa_colors =[colors2[key] for key in lsa_keys]
#get category and counts of documents in each category
lsa_categories, lsa_counts = keys_to_counts(lsa_keys)
#top words associated with each category
top_n_words_lsa = get_top_n_words(10, lsa_keys, dtm_tfidf, tf_vectorizer)

print("Topics \t Counts \t Top 10 Most Common Words for each Topic")
for i in range(len(top_n_words_lsa)):
    print("Topic {}: ".format(i), "Count: {0:1}".format(lsa_counts[i]), "\t", top_n_words_lsa[i])

#Plot Results
#Get compreesed vectors and words associated with each topic
top_3_words_lsa = get_top_n_words(3, lsa_keys, dtm_tfidf, tf_vectorizer)
lsa_mean_topic_vectors = get_mean_topic_vectors(lsa_keys, tsne_lsa_vectors)

#initialize Bokeh data structures with attributes - x, y, keys, colors
source = ColumnDataSource(data=dict(x=tsne_lsa_vectors[:,0].tolist(), y=tsne_lsa_vectors[:,1].tolist(), desc=lsa_keys,color=lsa_colors))
h = HoverTool(tooltips=[("Topic", "@desc"),("(x,y)", "($x, $y)")])
#create plot
plot = figure(title="Figure 2: t-Distributed Stochastic Neighbor Embedding (t-SNE) of {} LSA Topics".format(n_topics),
              plot_width=1000, plot_height=600, tools=["pan,wheel_zoom,box_zoom,reset",h],
              toolbar_location="below",x_axis_label=' Reduced Dimension 1', y_axis_label='Reduced Dimension 2')
#input points
plot.scatter(x='x', y='y', source=source, color='color')
#for i in range(tsne_lsa_vectors.shape[0]):
#    plot.scatter(x=tsne_lsa_vectors[i,0], y=tsne_lsa_vectors[i,1], color=colors[lsa_keys[i]])

#input words
for t in range(n_topics):
    label = Label(x=lsa_mean_topic_vectors[t][0], y=lsa_mean_topic_vectors[t][1],
                  text=top_3_words_lsa[t], text_color=color_text[t],render_mode='css',
                 text_font_size = '14pt', text_font_style = 'bold', x_offset=0, y_offset=0)
    plot.add_layout(label)

plot.xaxis.axis_label_text_font_size = "18pt"
plot.yaxis.axis_label_text_font_size = "18pt"
plot.title.text_font_size = "21pt"
plot.title_location = "above"
show(plot)
