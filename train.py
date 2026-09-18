import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATASET_PATH = "spam_dataset.csv"
MODEL_PATH = "spam_model.joblib"

df = pd.read_csv(DATASET_PATH)

X_train, X_test, y_train, y_test = train_test_split(df["text"],
                                                    df["label"],
                                                    test_size=0.2,
                                                    random_state=42,
                                                    stratify=df["label"])

model = Pipeline(
    [
        ("tfidf", TfidfVectorizer()),
        ("classifier", MultinomialNB()),
    ]
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Validation accuracy: {accuracy:.3f}")

joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")