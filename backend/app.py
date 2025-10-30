import os
import joblib
import re
import string
from flask import Flask, request, jsonify
from flask_cors import CORS
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import numpy as np

app = Flask(__name__)
CORS(app)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

try:
    stop_words = set(stopwords.words('indonesian'))
except:
    stop_words = {"yang", "untuk", "pada", "dan", "di", "ke", "dari"}

model_path = "model_naive_bayes.pkl"
vectorizer_path = "vectorizer.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    raise FileNotFoundError("❌ File model_naive_bayes.pkl atau vectorizer.pkl tidak ditemukan")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\@\w+|\#", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Teks tidak boleh kosong"}), 400

        cleaned_text = preprocess_text(text)
        X = vectorizer.transform([cleaned_text])
        pred = model.predict(X)[0]
        probs = model.predict_proba(X)[0]
        prob_max = round(max(probs) * 100, 2)

        # --- Hasil prediksi (0 = negatif, 1 = positif) ---
        sentiment_label = "POSITIF" if int(pred) == 1 else "NEGATIF"

        return jsonify({
            "text": text,
            "sentiment": sentiment_label,
            "probability": prob_max
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
