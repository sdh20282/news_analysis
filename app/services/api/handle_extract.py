import traceback
from pydantic import BaseModel

from app.enums.prompt import PromptType
from app.enums.model import LLMModelType
from app.schemas.json_response import JSONResponse
from app.schemas.model_response import SummaryResponse, EvaluationResponse
from app.services.extract.parser import extract_body_from_html
from app.services.llm.model import run_model_and_format_result

from app.utils.response import success_response, error_response


class ResponseContent(BaseModel):
    summary: SummaryResponse
    evaluation: EvaluationResponse


async def generate_data_from_url(url: str) -> JSONResponse[ResponseContent]:
    try:
        parseResult = await extract_body_from_html(url)

        if not parseResult.success:
            raise Exception(f"HTML 파싱 실패: {parseResult.message}")

        summaryResult = await run_model_and_format_result(
            PromptType.SUMMARY,
            LLMModelType.LLAMA,
            SummaryResponse,
            parseResult.data,
        )

        if not summaryResult.success:
            raise Exception(f"요약 실패: {summaryResult.message}")

        evalResult = await run_model_and_format_result(
            PromptType.EVALUATION,
            LLMModelType.LLAMA,
            EvaluationResponse,
            summaryResult.data,
        )

        if not evalResult.success:
            raise Exception(f"평가 실패: {evalResult.message}")

        return success_response(
            message="URL 내용 추출 성공",
            data=ResponseContent(
                summary=summaryResult.data,
                evaluation=evalResult.data,
            ),
        )
    except Exception as e:
        print("[ERROR] app/services/api/handle_excract.py 예외 발생:", e)
        print(f"URL: {url}")

        traceback.print_exc()

        return error_response(
            message="URL 내용 추출 실패",
        )
