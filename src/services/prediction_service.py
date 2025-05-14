import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

class CategoryClassifier:
    def __init__(self):
        self.model = joblib.load("src/models/category_classifier.joblib")
        self.vectorizer = joblib.load("src/models/tfidf_vectorizer.joblib")

    def predict_category(self, title: str, description: str) -> str:
        text = title + " " + description
        text_vec = self.vectorizer.transform([text])
        return self.model.predict(text_vec)[0]