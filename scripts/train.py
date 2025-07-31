import json
import numpy as np
import logging
import re

from pathlib import Path
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

LOG_PATH = "logs/train.log"


class RemoveANSICodeFilter(logging.Filter):
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.ansi_escape.sub("", str(record.msg))
        return True


file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
file_handler.addFilter(RemoveANSICodeFilter())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        file_handler,
    ],
)

logger = logging.getLogger(__name__)


def load_model(model_type="simple_dense", input_shape=(128,), output_dim=3):
    if model_type == "simple_dense":
        model = tf.keras.Sequential(
            [
                layers.Input(shape=input_shape),
                layers.Dense(128, activation="relu"),
                layers.Dropout(0.3),
                layers.Dense(output_dim, activation="softmax"),
            ]
        )
    elif model_type == "cnn_text":
        model = tf.keras.Sequential(
            [
                layers.Embedding(
                    input_dim=10000, output_dim=128, input_length=input_shape[0]
                ),
                layers.Conv1D(128, 5, activation="relu"),
                layers.GlobalMaxPooling1D(),
                layers.Dense(output_dim, activation="softmax"),
            ]
        )
    else:
        raise ValueError(f"지원하지 않는 모델 타입입니다: {model_type}")

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model


def load_dataset(path: str, max_len: int = 128):
    texts = []
    labels = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["text"])
            labels.append(
                [
                    obj["label"]["positive"],
                    obj["label"]["negative"],
                    obj["label"]["neutral"],
                ]
            )

    return texts, labels


def main():
    dataset_path = "data/uploads/uploaded_data.jsonl"

    if not Path(dataset_path).exists():
        logger.error("학습 데이터 파일이 존재하지 않습니다.")
        return

    logger.info("데이터 로딩 중...")
    texts, labels = load_dataset(dataset_path)

    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=128, padding="post")

    X = np.array(padded)
    y = np.array(labels)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    logger.info(f"학습 샘플 수: {len(X_train)}, 검증 샘플 수: {len(X_val)}")

    model = load_model(model_type="simple_dense", input_shape=(128,), output_dim=3)

    logger.info("학습 시작")
    model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        verbose=2,
    )
    logger.info("학습 완료")

    model.save("models/finetuned_model.keras")

    logger.info("모델 저장 완료: models/finetuned_model")


if __name__ == "__main__":
    main()
