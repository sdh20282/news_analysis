from pydantic import BaseModel


class SummaryResponse(BaseModel):
    content: str
    summary: str


class EvaluationResponse(BaseModel):
    positive: int
    negative: int
    neutral: int
