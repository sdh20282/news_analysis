import httpx
import traceback

from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


async def generate_llama3_response(prompt: str) -> JSONResponse[str]:
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "format": "json",
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, json=payload, timeout=300)
            response.raise_for_status()

            result = response.json()
            llama_response_data = result.get("response", "")

            if not llama_response_data:
                print(f"[WARN] Llama3 응답 데이터 없음: {result}")

                return error_response(
                    message="Llama3 모델로부터 유효한 응답을 받지 못했습니다.",
                )

            return success_response(
                message="응답 생성 성공",
                data=llama_response_data,
            )
        except Exception as e:
            print(f"[ERROR] app/services/llm/ollama/llama3.py 예외 발생: {e}")
            print(f"PROMPT : {prompt}")

            traceback.print_exc()
            return error_response(
                message="응답 생성 중 예상치 못한 오류 발생",
            )
