import pickle

import gensim
import numpy as np
import pandas as pd
from gensim.models import FastText
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""
Training models file:
    - This file is for generating the similarity and linear regression models
"""

df = pd.read_csv("cleaned_job_listings.csv")


# Preprocess text function
def preprocess_text(text):
    return gensim.utils.simple_preprocess(text, deacc=True, min_len=3)


sentences = df["Title"].apply(preprocess_text).tolist()

ft_model = FastText(
    sentences, vector_size=300, window=5, min_count=1, workers=4, sg=1, epochs=10
)

ft_model.save("desc_FT_new.model")


def get_vector(text, model):
    tokens = preprocess_text(text)
    vector = np.mean([model.wv[token] for token in tokens if token in model.wv], axis=0)
    if np.isnan(vector).any():
        vector = np.zeros(model.vector_size)
    return vector


X = np.array(df["Title"].apply(lambda x: get_vector(x, ft_model)).tolist())
y = df["Category"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)

y_pred = lr_model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

with open("descFT_LR_new.pkl", "wb") as f:
    pickle.dump(lr_model, f)


# Use the new models for job search and recommendation
def search_jobs(keyword, df, ft_model, scaler, threshold=0.7):
    keyword_vector = get_vector(keyword, ft_model)
    keyword_vector = scaler.transform([keyword_vector])[0]
    results = []

    for index, row in df.iterrows():
        job_title_vector = get_vector(row["Title"], ft_model)
        job_title_vector = scaler.transform([job_title_vector])[0]
        similarity = np.dot(keyword_vector, job_title_vector) / (
            np.linalg.norm(keyword_vector) * np.linalg.norm(job_title_vector)
        )

        if similarity > threshold:
            results.append((index, row["Title"], similarity))

    return sorted(results, key=lambda x: x[2], reverse=True)
