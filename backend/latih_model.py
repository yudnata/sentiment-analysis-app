import pandas as pd
import re
import nltk
import joblib
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

try:
    stopwords_indonesia = stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')
    stopwords_indonesia = stopwords.words('indonesian')

def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # hapus link
    text = re.sub(r'\@\w+|\#', '', text)  # hapus mention dan tagar
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # hapus simbol
    text = text.lower()
    words = text.split()
    important_words = {'tidak', 'sangat', 'sekali'}
    filtered_words = [w for w in words if w not in stopwords_indonesia or w in important_words]
    return ' '.join(filtered_words)

file_path = './dataset/dataset-sentimen-analisis-v3.csv'
df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

print("Kolom terdeteksi:", df.columns.tolist())

df.columns = [col.strip().lower() for col in df.columns]
if 'text' not in df.columns or 'sentiment' not in df.columns:
    raise ValueError("❌ Kolom 'text' dan 'sentiment' tidak ditemukan di dataset!")

df['text_bersih'] = df['text'].apply(preprocess_text)
df.dropna(subset=['text_bersih', 'sentiment'], inplace=True)
df = df[df['text_bersih'].str.strip() != '']

df['sentiment'] = df['sentiment'].astype(int)
df = df[df['sentiment'].isin([0, 1])]

X_train, X_test, y_train, y_test = train_test_split(df['text_bersih'], df['sentiment'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print("=== Laporan Akurasi Model ===")
print(classification_report(y_test, y_pred, target_names=['Negatif', 'Positif']))

joblib.dump(model, 'model_naive_bayes.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("✅ Model dua kelas berhasil disimpan ke model_naive_bayes.pkl & vectorizer.pkl")
