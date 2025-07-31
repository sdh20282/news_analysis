import httpx
from bs4 import BeautifulSoup
import traceback

from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


async def extract_body_from_html(url: str, timeout: int = 10) -> JSONResponse[str]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MyParserBot/1.0)"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            body = soup.body

            result = body.get_text(separator="\n", strip=True) if body else ""

            if not result:
                print(f"[WARN] URL ({url})에서 HTML body 내용이 비어 있습니다.")

                return error_response(
                    message="URL에서 HTML body 내용을 추출할 수 없습니다."
                )

            return success_response(
                message="HTML 파싱 성공",
                data=result,
            )
        except Exception as e:
            print(
                f"[ERROR] app/services/parser/html_parser.py 예외 발생 - URL: {url}, 오류: {e}"
            )

            traceback.print_exc()

            return error_response(message="HTML 파싱 중 예상치 못한 오류 발생")
