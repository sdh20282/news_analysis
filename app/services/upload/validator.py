from app.services.upload.formatter import normalize_scores, to_json_line


def validate_row(row, colMap):
    if all(cell.value is None for cell in row):
        return None

    number = row[colMap["번호"]].value
    text = row[colMap["본문"]].value
    pos = row[colMap["긍정"]].value
    neg = row[colMap["부정"]].value
    neu = row[colMap["중립"]].value

    if text is None or any(v is None for v in [pos, neg, neu]):
        raise ValueError(f"필드 누락 : {number} 행")

    if not all(isinstance(v, (int, float)) for v in [pos, neg, neu]):
        raise ValueError(f"감정 점수 숫자 형식에 맞지 않음 : {number} 행")

    pos_ratio, neg_ratio, neu_ratio = normalize_scores(pos, neg, neu)

    return to_json_line(text, pos_ratio, neg_ratio, neu_ratio)
