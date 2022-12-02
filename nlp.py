from keybert import KeyBERT
import spacy #natural language processing
from spacy.tokens import Doc
import en_core_web_sm
import pandas as pd
import csv
import codecs
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import tokenize # fast sentence tokenization
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from collections import Counter
nltk.download('wordnet')
nltk.download('omw-1.4')
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline


df = pd.read_csv("data/files/CMS_PUBLIC_COMMENTS_2022_7-9.csv")
df = df.dropna(thresh=df.shape[0]*0.8, axis=1)
df = df.dropna(subset=['Comment'])
df.drop_duplicates(subset=["Comment"], keep='first', inplace=True)
comments = df['Comment'].to_numpy() # extract all comments into an array
#
# tknzr = TweetTokenizer()
# nlp = spacy.load("en_core_web_sm") # NLP for english
# lemmatizer = WordNetLemmatizer()
#
# # customized a class for tweet tokenizer
# def tweet_tokenize(x):
#     return Doc(nlp.vocab, words = tknzr.tokenize(x))
#
# # set our nlp pipeline with tokenizer specialized for tweets
# nlp.tokenizer = tweet_tokenize
#
# processed_comments = []
#
# # count top words in different categories
# all_counter = Counter()
# adj_counter = Counter()
# noun_counter = Counter()
# verb_counter = Counter()
#
# useful_words = []
# adjs = []
# nouns = []
# verbs = []
#
# remove_words = ['<br/>']
#
# entity_list = []
#
# # loop over each comment
# for comment in comments:
#
#     processed_comment = []
#
#     # Convert comment into Doc object with a sequence of tokens
#     for token in nlp(str(comment).lower()):
#         if token.text in nlp.Defaults.stop_words or 'http' in token.text or token.text in string.punctuation or len(
#                 token.text) < 2 or token.text in remove_words:  # remove stop words
#             continue
#         else:
#             useful_words.append(token.text)
#             processed_comment.append(lemmatizer.lemmatize(token.text))
#         if token.pos_ == 'ADJ':
#             adjs.append(token.text)
#         elif token.pos_ == 'NOUN':
#             nouns.append(token.text)
#         elif token.pos_ == 'VERB':
#             verbs.append(token.text)
#
#     for x in nlp(str(comment).lower()).ents:
#         if len(x.text) < 2 or x.text.isnumeric():
#             continue
#         else:
#             entity_list.append(x.text.lower())
#
#     processed_comments.append(' '.join(processed_comment))
#
# all_counter.update(useful_words)
# adj_counter.update(adjs)
# noun_counter.update(nouns)
# verb_counter.update(verbs)
#
# print('Overall Top 20:\n')
# print(all_counter)
# print(all_counter.most_common(20))
# print('-----------------------------------\n')
# print('Adjectives Top 10:\n')
# print(adj_counter.most_common(10))
# print('-----------------------------------\n')
# print('Nouns Top 10:\n')
# print(noun_counter.most_common(10))
# print('-----------------------------------\n')
# print('Verbs Top 10:\n')
# print(verb_counter.most_common(10))

kw_model = KeyBERT()
all_comments = ""
for i in range(0, len(df['Comment'])):
   all_comments = all_comments  + " " + str(df['Comment'].iloc[i])

keywords_comments = kw_model.extract_keywords(all_comments, keyphrase_ngram_range=(1, 3), top_n=20)
print(keywords_comments)
#
# # Extract keywords from each comment
#
# comments = df['Comment'].to_numpy() # extract all comments into an array
# keywords = kw_model.extract_keywords(comments,keyphrase_ngram_range=(1, 2), stop_words=None)
# print(keywords)

# from wordcloud import WordCloud
# from wordcloud import STOPWORDS
#
# # Wordcloud with all comments
# comments = df['Comment']
# stop_words = ["https", "co", "RT"] + list(STOPWORDS)
# wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords=stop_words,
#                       collocation_threshold=3).generate(str(comments))
# plt.figure()
# plt.title("All Comments - Wordcloud")
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()