import traceback

from app.enums.prompt import PromptType
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


SUMMARY_TEMPLATE = """
    This is the result of parsing a news html. I'll tell you what to do from now on.

    1. From the parsing results I delivered, I skip the useless parts except the news body, and only make the news body in text form.
    2. Summarize the news body generated in step 1 at least 200 to 300 characters. The whole content should not be distorted in this process. And I hope it's word-oriented if possible.

    Output must be valid JSON, exactly matching this format:
    {"content": "<Stage 1 result>", "summary": "<Stage 2 result>"}

    Do not add explanations, comments, or markdown.
    Here is the parsed result:
""".strip()

EVALUATION_TEMPLATE = """
    You will be given a news summary. Determine the sentiment distribution in % for positive, negative, and neutral. 
    The total must be exactly 100.

    Output must be valid JSON, exactly matching this format:
    {"positive": <int>, "negative": <int>, "neutral": <int>}

    Do not add explanations, comments, or markdown.
    Here is the summary:
""".strip()


async def generate_prompt(type: PromptType, content: str) -> JSONResponse[str]:
    try:
        promptMap = {
            PromptType.SUMMARY: lambda c: f"{SUMMARY_TEMPLATE}\n\n{c}",
            PromptType.EVALUATION: lambda c: f"{EVALUATION_TEMPLATE}\n\n{c}",
        }

        promptFn = promptMap.get(type)

        if not promptFn:
            raise Exception(f"프롬프트 생성 타입이 맞지 않음 : {type}")

        prompt = promptFn(content)

        return success_response(
            message="프롬프트 생성 성공",
            data=prompt,
        )
    except Exception as e:
        print("[ERROR] app/utils/prompt.py 예외 발생:", e)

        traceback.print_exc()

        return error_response(
            message="프롬프트 생성 실패",
        )
