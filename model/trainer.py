import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib


# Data import

df = pd.read_csv("../data/Final_Amharic.csv")

# Feature and Target Separation

df["text"] = df["headline"] + " " + df["article"] + " " + df["link"]

X = df.text
y = df.category

# Splitting Data to Training and Testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization, Standardization, and Training Pipeline

model = make_pipeline(
	TfidfVectorizer(max_features=5000),
	StandardScaler(with_mean=False),
	LogisticRegression(
		C=0.1,
		max_iter=1000,
		random_state=42
	)
)


# Model Training


model.fit(X_train, y_train)


# Testing Model on Training and Test Datas

print(f"Training accuracy: {model.score(X_train, y_train):.2f}"),
print(f"Test accuracy: {model.score(X_test, y_test):.2f}")


# Extraction of vectorizer and model

joblib.dump(model, "news_classfier_pipeline.pkl")