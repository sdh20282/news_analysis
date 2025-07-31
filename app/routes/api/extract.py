from fastapi import APIRouter, Request

import traceback

from app.schemas.json_response import JSONResponse
from app.services.api.handle_extract import generate_data_from_url, ResponseContent
from app.utils.response import success_response, error_response


router = APIRouter()


@router.post("", response_model=JSONResponse[ResponseContent])
async def extract(request: Request):
    try:
        body = await request.json()
        url = body.get("url")

        if not url:
            raise Exception("URL 값 없음")

        extract_result = await generate_data_from_url(url)

        return success_response(
            message="데이터 추출 성공",
            data=extract_result.data,
        )
    except Exception as e:
        print("[ERROR] app/routes/api/excract.py 예외 발생:", e)
        print(f"URL: {url}")

        traceback.print_exc()

        return error_response(
            message="데이터 추출 실패",
        )
