import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import mlflow

def train_model():
    mlflow.set_experiment("YouTube Category Classification")
    
    with mlflow.start_run():
        # ... (previous code)
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_artifact("src/models/tfidf_vectorizer.joblib")

df = pd.read_json("src/data/labeled_videos.json")
df.to_csv("src/data/labeled_videos.csv", index=False)

def train_model(data_path: str = "src/data/labeled_videos.csv"):
    # Load data (columns: "title", "description", "category")
    df = pd.read_csv(data_path)
    df["text"] = df["title"] + " " + df["description"]  # Combine features

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["category"], test_size=0.2, random_state=42
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    # Evaluate
    y_pred = model.predict(X_test_vec)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Save model and vectorizer
    os.makedirs("src/models", exist_ok=True)
    joblib.dump(model, "src/models/category_classifier.joblib")
    joblib.dump(vectorizer, "src/models/tfidf_vectorizer.joblib")

if __name__ == "__main__":
    train_model()