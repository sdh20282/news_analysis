from pydantic import BaseModel


class ResponseContentHandleExtract(BaseModel):
    result: str


class ResponseContentLLM(BaseModel):
    result: str


class ResponseContentParseURL(BaseModel):
    result: str
