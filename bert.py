from keybert import KeyBERT
import pandas as pd
kw_model = KeyBERT()
all_comments = ""
df = pd.read_csv("data/files/CMS_PUBLIC_COMMENTS_2022_7-9.csv")

for i in range(0,len(df['Comment'])):
   all_comments  = all_comments  + " " + str(df['Comment'].iloc[i])

keywords_comments = kw_model.extract_keywords(all_comments,keyphrase_ngram_range=(1, 2), stop_words=None)
import pickle
pickle.dump(keywords_comments, open('model/keywords_comments.pkl', 'wb'))
