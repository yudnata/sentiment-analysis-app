# backend/latih_model.py
import pandas as pd
import re
import nltk
import joblib
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- Unduh stopwords ---
try:
    stopwords_indonesia = stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')
    stopwords_indonesia = stopwords.words('indonesian')

# --- Fungsi Preprocessing ---
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    words = text.split()
    important_words = {'tidak', 'sangat', 'sekali'}
    filtered_words = [w for w in words if w not in stopwords_indonesia or w in important_words]
    return ' '.join(filtered_words)

# --- Muat dataset ---
df = pd.read_csv('./dataset/INA_TweetsPPKM_Labeled_Pure.csv', encoding='utf-8', sep='\t', on_bad_lines='skip')

df['Tweet_bersih'] = df['Tweet'].apply(preprocess_text)
label_mapping = {0: 'positif', 1: 'netral', 2: 'negatif'}
df['Sentiment_text'] = df['sentiment'].map(label_mapping)

df.dropna(subset=['Tweet_bersih', 'Sentiment_text'], inplace=True)
df = df[df['Tweet_bersih'] != '']

texts = df['Tweet_bersih'].tolist()
labels = df['Sentiment_text'].tolist()

# --- Latih model ---
vectorizer = CountVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(texts)
classifier = MultinomialNB()
classifier.fit(X, labels)

# --- Simpan model & vectorizer ---
joblib.dump(classifier, 'model_naive_bayes.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("✅ Model dan vectorizer berhasil disimpan ke model_naive_bayes.pkl & vectorizer.pkl")
