import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib


def create_model(X_train, X_test, y_train, y_test):

	model = make_pipeline(
	    TfidfVectorizer(max_features=5000),
	    StandardScaler(with_mean=False),
	    LogisticRegression(
	        C=0.1,
	        max_iter=1000,
	        random_state=42
	    )
	)

	fitted_model = model.fit(X_train, y_train)

	print(f"Training Accuracy: {model.score(X_train, y_train)}")
	print(f"Test Accuracy: {model.score(X_test, y_test)}")

	return fitted_model


# Amharic Model Training

df = pd.read_csv("../data/Amharic.csv")

df["text"] = df.headline + " " + df.article + " " + df.link

X = df.text
y = df.category

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Amharic Model Training!")

amharic_model = create_model(X_train, X_test, y_train, y_test)

joblib.dump(amharic_model, "Amharic_Classification_Pipeline.pkl")


# English Model Training

df = pd.read_csv("../data/English.csv")

X = df.text
y = df.category

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("English Model Training!")

english_model = create_model(X_train, X_test, y_train, y_test)

joblib.dump(english_model, "English_Classification_Pipeline.pkl")