from typing import TypeVar

from app.schemas.json_response import JSONResponse

T = TypeVar("T")


def success_response(data: T, message: str = "") -> JSONResponse[T]:
    return JSONResponse(success=True, message=message, data=data)


def error_response(message: str) -> JSONResponse[None]:
    return JSONResponse(success=False, message=message, data=None)
