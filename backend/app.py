# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib
import nltk
from nltk.corpus import stopwords

# --- Load Stopwords ---
try:
    stopwords_indonesia = stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')
    stopwords_indonesia = stopwords.words('indonesian')

# --- Inisialisasi Flask ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# --- Load Model & Vectorizer ---
try:
    classifier = joblib.load('model_naive_bayes.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    print("✅ Model dan vectorizer berhasil dimuat")
except Exception as e:
    print(f"❌ Gagal memuat model/vectorizer: {e}")
    classifier, vectorizer = None, None

# --- Preprocessing ---
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    words = text.split()
    important_words = {'tidak', 'sangat', 'sekali'}
    filtered_words = [w for w in words if w not in stopwords_indonesia or w in important_words]
    return ' '.join(filtered_words)

# --- Rule-Based Filter ---
def check_simple_rules(text):
    positives = ["kerja bagus", "bagus sekali", "sangat baik", "terbaik", "luar biasa", "hebat", "mantap"]
    negatives = ["buruk", "mengecewakan", "tidak berguna", "parah", "payah", "jelek"]
    for p in positives:
        if p in text:
            return "positif"
    for n in negatives:
        if n in text:
            return "negatif"
    return None

# --- Endpoint Analisis ---
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Teks tidak ditemukan'}), 400

    if classifier is None or vectorizer is None:
        return jsonify({'error': 'Model belum dimuat'}), 500

    text = data['text'].lower()
    rule_result = check_simple_rules(text)
    if rule_result:
        return jsonify({'sentiment': rule_result, 'probability': 1.0})

    cleaned = preprocess_text(text)
    X_new = vectorizer.transform([cleaned])
    prediction = classifier.predict(X_new)[0]
    probabilities = classifier.predict_proba(X_new)[0]
    max_prob = float(max(probabilities))

    return jsonify({'sentiment': prediction, 'probability': max_prob})

if __name__ == '__main__':
    app.run(debug=True, port=50000)
