import json
from pydantic import BaseModel

from google import genai

from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


API_KEY = "AIzaSyCQisQH-iPwgThbv2mEQPdox8qCqfOIs70"

client = genai.Client(api_key=API_KEY)


async def generate_gemini_flash_response(
    prompt: str, schema: BaseModel
) -> JSONResponse[str]:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        result = response.json()

        parsed = json.loads(result)

        text = (
            parsed.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        return success_response(
            message="응답 생성 성공",
            data=text,
        )
    except Exception as e:
        print("[EXCEPTION] 예외 발생:", e)

        return error_response(
            message=f"예상치 못한 오류가 발생했습니다: {str(e)}",
        )
