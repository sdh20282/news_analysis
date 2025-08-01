import pickle

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from app.schemas.model_response import EvaluationResponse

model = load_model("models/finetuned_model.keras")

with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)


def predict_sentiment(text: str, max_len: int = 128) -> list[float]:
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=max_len, padding="post")
    prediction = model.predict(padded)[0]

    percent = [round(p * 100) for p in prediction]

    return EvaluationResponse(
        positive=percent[0],
        negative=percent[1],
        neutral=percent[2],
    )
