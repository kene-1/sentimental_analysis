# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iB7oTaJdmZ3xmfYlhhjGyI_lbfJ6YRI8
"""

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from sklearn.utils import resample
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer as tf
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve
from string import punctuation
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.calibration import CalibratedClassifierCV

# Load and preprocess the train dataset
df_train = pd.read_csv('train.csv', delimiter=',', encoding='latin-1')
df_train.columns = ['textID','text','selected_text','sentiment','Time of Tweet','Age of User','Country','Population -2020','Land Area (Km²)','Density (P/Km²)']
df_train = df_train.dropna(subset=['text', 'selected_text'])
df_train['sentiment'] = df_train['sentiment'].replace({4:1})

# Text processing function
def textprocessing(text):
    text = str(text).lower()
    text = re.sub(r"https\S+|www\S+|https\S+"," ",text,flags=re.MULTILINE)
    text=re.sub("(\\d|\\W)+"," ",text)
    text = re.sub(r'\@\w+|\#'," ",text)
    text = re.sub(r'[^\w\s\`]'," ",text)
    text_tokens = word_tokenize(text)
    lem = SnowballStemmer("english")
    text = [lem.stem(word) for word in text_tokens if not word in list(punctuation)]
    text1 = " ".join(text)
    return text1

df_train['text'] = df_train['text'].apply(textprocessing)
df_train = df_train[['sentiment','text']]

# Feature extraction
vectorizer = tf()
vectors_train = vectorizer.fit_transform(df_train['text'])

# Split the train dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(vectors_train, df_train['sentiment'], test_size=0.3, random_state=52)

# Train the model
classifier = CalibratedClassifierCV(LinearSVC(dual=True), method='sigmoid')
classifier.fit(X_train, y_train)

# Evaluate the model on the training set
svm_predictions_train = classifier.predict(X_train)
accuracy_train = accuracy_score(y_train, svm_predictions_train)
print(f"Training Accuracy: {accuracy_train:.2f}")
print("Training Classification Report:")
print(classification_report(y_train, svm_predictions_train))

# Load and preprocess the test dataset
df_test = pd.read_csv('test.csv', delimiter=',', encoding='latin-1')
df_test.columns = ['textID','text','sentiment','Time of Tweet','Age of User','Country','Population -2020','Land Area (Km²)','Density (P/Km²)']
df_test = df_test.dropna(subset=['text', 'sentiment'])

# Apply the same text processing function
df_test['text'] = df_test['text'].apply(textprocessing)
df_test = df_test[['text','sentiment']]

# Feature extraction for the test dataset
vectors_test = vectorizer.transform(df_test['text'])

# Make predictions on the test dataset
svm_predictions_test = classifier.predict(vectors_test)

#Assuming you have the true labels for the test dataset, you can evaluate the model
#For example, if you have a DataFrame `df_test_labels` with the true labels:
y_test = df_test['sentiment']
accuracy_test = accuracy_score(y_test, svm_predictions_test)
print(f"Testing Accuracy: {accuracy_test:.2f}")
print("Testing Classification Report:")
print(classification_report(y_test, svm_predictions_test))