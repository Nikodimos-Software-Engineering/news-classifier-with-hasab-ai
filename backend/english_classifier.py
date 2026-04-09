import joblib

model = joblib.load("../model/English_Classification_Pipeline.pkl")

def get_english_classification(text):

    pred = model.predict([text])
    pred_proba = model.predict_proba([text])

    confidence = max(pred_proba[0]) * 100

    return pred[0], confidence
