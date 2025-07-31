import traceback
from pydantic import BaseModel

from app.enums.prompt import PromptType
from app.services.extract.parser import extract_body_from_html
from app.services.prompt.prompt import generate_prompt
from app.services.llm.ollama.llama3 import generate_llama3_response
from app.services.llm.gemini.gemini_flash import generate_gemini_flash_response
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


class SummaryResponse(BaseModel):
    content: str
    summary: str


class EvaluationResponse(BaseModel):
    positive: int
    negative: int
    neutral: int


class ResponseContent(BaseModel):
    content: str
    summary: str
    evaluation: EvaluationResponse


async def fetch_and_parse_url(url: str) -> str:
    result = await extract_body_from_html(url)

    if not result.success:
        raise Exception(f"HTML 파싱 실패: {result.message}")

    return result.data


async def get_response_from_llama3(type: PromptType, content: str):
    prompt = await generate_prompt(type, content)

    if not prompt.success:
        raise Exception(f"${type} 프롬프트 생성 실패: {prompt.message}")

    return await generate_llama3_response(prompt.data)


async def get_summary_from_llama3(content: str) -> SummaryResponse:
    result = await get_response_from_llama3(PromptType.SUMMARY, content)

    return SummaryResponse.parse_raw(result.data)


async def get_evaluation_from_llama3(summary: str) -> EvaluationResponse:
    result = await get_response_from_llama3(PromptType.EVALUATION, summary)

    return EvaluationResponse.parse_raw(result.data)


async def get_response_from_gemini_flash(
    type: PromptType, content: str, schema: BaseModel = None
):
    prompt = await generate_prompt(type, content)

    if not prompt.success:
        raise Exception(f"${type} 프롬프트 생성 실패: {prompt.message}")

    return await generate_gemini_flash_response(prompt.data, schema)


async def get_summary_from_gemini_flash(content: str) -> SummaryResponse:
    result = await get_response_from_gemini_flash(
        PromptType.SUMMARY, content, SummaryResponse
    )

    return SummaryResponse.parse_raw(result.data)


async def get_evaluation_from_gemini_flash(summary: str) -> EvaluationResponse:
    result = await get_response_from_gemini_flash(
        PromptType.EVALUATION, summary, EvaluationResponse
    )

    return EvaluationResponse.parse_raw(result.data)


async def generate_data_from_url(url: str) -> JSONResponse[ResponseContent]:
    try:
        content = await fetch_and_parse_url(url)
        summaryData = await get_summary_from_llama3(content)
        evalData = await get_evaluation_from_llama3(summaryData.summary)

        return success_response(
            message="URL 내용 추출 성공",
            data=ResponseContent(
                content=summaryData.content,
                summary=summaryData.summary,
                evaluation=evalData,
            ),
        )
    except Exception as e:
        print("[ERROR] app/services/api/handle_excract.py 예외 발생:", e)
        print(f"URL: {url}")

        traceback.print_exc()

        return error_response(
            message="URL 내용 추출 실패",
        )
