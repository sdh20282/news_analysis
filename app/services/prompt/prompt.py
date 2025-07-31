import traceback

from app.enums.prompt import PromptType
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


SUMMARY_TEMPLATE = """
    This is the result of parsing a news story. I'll tell you what to do from now on.

    1. From the parsing results I delivered, I skip the useless parts except the news body, and only make the news body in text form.
    2. Summarize the news body generated in step 1 at least 200 to 300 characters. The whole content should not be distorted in this process. And I hope it's word-oriented if possible.

    Please return the results of step 1 and 2 in json format. The format is as follows.

    {
      "content": Stage 1 results,
      "summary": Stage 2 results
    }

    I'll put the parsed result on the bottom. You can analyze it after the sentence. Respond using JSON format.
""".strip()

EVALUATION_TEMPLATE = """
    The text below summarizes news articles. Based on this, please determine whether the article is positive, negative, or neutral. At this time, positive, negative, and neutral should be expressed in % respectively, and the sum of positive%, negative%, and neutral should be 100%.

    Please return the result after organizing it in json format. The format is as follows.

    {
      "positive": positive %,
      "native": negative %,
      "neutral": neutral %
    }

    I'll put the summary on the bottom. You can analyze it after the sentence. Respond using JSON format.
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
