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