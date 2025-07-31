import os

UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_output_path():
    return os.path.join(UPLOAD_DIR, "uploaded_data.jsonl")


def open_output_stream(file_path):
    return open(file_path, "w", encoding="utf-8")
