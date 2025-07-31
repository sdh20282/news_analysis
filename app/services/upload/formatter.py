import json


def normalize_scores(pos, neg, neu):
    total = pos + neg + neu
    if total == 0:
        return 1 / 3, 1 / 3, 1 / 3
    return pos / total, neg / total, neu / total


def to_json_line(text, pos_ratio, neg_ratio, neu_ratio) -> str:
    return json.dumps(
        {
            "text": text,
            "label": {
                "positive": pos_ratio,
                "negative": neg_ratio,
                "neutral": neu_ratio,
            },
        },
        ensure_ascii=False,
    )
