# Copyright Chathika Gunaratne <chathikagunaratne@gmail.com>
# This script analyzes data from the tweet ids provided in https://github.com/echen102/COVID-19-TweetIDs

import pandas as pd
from numpy import genfromtxt
import numpy as np
from glob import glob
import os
import spacy
from sklearn.cluster import DBSCAN
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

tweet_files = glob ("echen102_COVID-19-TweetIDs_Tweets/*.jsonl.gz")

all_tweet_data = []
i = 0
for tweet_file in tqdm(tweet_files):
    try:
        all_tweet_data.extend(pd.read_json(tweet_file,lines=True)[["created_at","full_text"]].values.tolist())
    except:
        print(tweet_file)
        pass

print(all_tweet_data)

df = pd.DataFrame(all_tweet_data,columns=["created_at","full_text"])
nlp = spacy.load('en_core_web_sm')

sent_vecs = {}
docs = []

for text in df.full_text:
    doc = nlp(text)
    docs.append(doc)
    sent_vecs.update({text: doc.vector})

sentences = list(sent_vecs.keys())
vectors = list(sent_vecs.values())

x = np.array(vectors)
n_classes={}
for i in tqdm(np.arange(0.001, 1, 0.002)):
    dbscan = DBSCAN(eps=i, min_samples=2, metric="cosine").fit(x)
    n_classes.update({i: len(pd.Series(dbscan.labels_).value_counts())})

eps_clusters = pd.DataFrame(list(n_classes.items()), columns = ["Epsilon","Clusters"])
sns.lineplot(data = eps_clusters, x = "Epsilon", y = "Clusters")

dbscan = DBSCAN(eps=0.065, min_samples=2, metric="cosine").fit(x)

results = pd.DataFrame({"label": dbscan.labels_, "sent": sentences})
example_result = results[results.label == 25].sent.tolist()
event_df = df[df.full_text.isin(example_result)][["created_at", "full_text"]]
event_df["created_at"] = pd.to_datetime(event_df.created_at)
event_df = event_df.sort_values(by = "created_at").dropna()


