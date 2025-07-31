import traceback

from app.enums.prompt import PromptType
from app.enums.model import LLMModelType
from app.services.llm.ollama.llama3 import generate_llama3_response
from app.services.llm.gemini.gemini_flash import generate_gemini_flash_response
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


async def get_response_from_gemini(
    type: PromptType, content: str, schema: BaseModel = None
):
    prompt = await generate_prompt(type, content)

    if not prompt.success:
        raise Exception(f"${type} 프롬프트 생성 실패: {prompt.message}")

    return await generate_gemini_flash_response(prompt.data, schema)


async def get_summary_model(type: LLMModelType):
    try:
        modelMap = {
            LLMModelType.GEMINI: generate_gemini_flash_response,
            LLMModelType.LLAMA: generate_llama3_response,
        }

        modelFn = modelMap.get(type)

        if not modelFn:
            raise Exception(f"모델 생성 타입이 맞지 않음 : {type}")

        return success_response(
            message="프롬프트 생성 성공",
            data=modelFn,
        )
    except Exception as e:
        print("[ERROR] app/utils/prompt.py 예외 발생:", e)

        traceback.print_exc()

        return error_response(
            message="프롬프트 생성 실패",
        )
