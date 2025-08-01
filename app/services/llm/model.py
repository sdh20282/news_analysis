import traceback

from pydantic import BaseModel
from typing import Callable, Awaitable

from app.enums.prompt import PromptType
from app.enums.model import LLMModelType
from app.services.prompt.prompt import generate_prompt
from app.services.llm.ollama.llama3 import generate_llama3_response
from app.services.llm.gemini.gemini_flash import generate_gemini_flash_response
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


async def get_model(
    type: LLMModelType,
) -> JSONResponse[Callable[[str, BaseModel], Awaitable[JSONResponse[str]]]]:
    try:
        modelMap = {
            LLMModelType.GEMINI: generate_gemini_flash_response,
            LLMModelType.LLAMA: generate_llama3_response,
        }

        modelFn = modelMap.get(type)

        if not modelFn:
            raise Exception(f"모델 생성 타입이 맞지 않음 : {type}")

        return success_response(
            message="모델 생성 성공",
            data=modelFn,
        )
    except Exception as e:
        print("[ERROR] app/services/llm/model.py - get_model 예외 발생:", e)

        traceback.print_exc()

        return error_response(
            message="모델 생성 실패",
        )


async def run_model(
    type: LLMModelType,
    schema: BaseModel,
    prompt: str,
) -> JSONResponse[str]:
    try:
        modelResult = await get_model(type)

        if not modelResult.success:
            raise Exception(f"${type} 모델 생성 실패: {modelResult.message}")

        modelFn = modelResult.data

        if not modelFn:
            raise Exception(f"모델 함수가 존재하지 않음 : {type}")

        runResult = await modelFn(prompt, schema)

        if not runResult.success:
            raise Exception(f"학습 결과 오류 : {runResult.message}")

        return success_response(
            message="모델 실행 성공",
            data=runResult.data,
        )
    except Exception as e:
        print("[ERROR] app/services/llm/model.py - run_model 예외 발생:", e)

        traceback.print_exc()

        return error_response(
            message="모델 실행 실패",
        )


async def run_model_and_format_result(
    promptType: PromptType,
    llmType: LLMModelType,
    schema: BaseModel,
    content: str,
) -> JSONResponse[str]:
    try:
        promptResult = await generate_prompt(promptType, content)

        if not promptResult.success:
            raise Exception(f"${promptType} 프롬프트 생성 실패: {promptResult.message}")

        runResult = await run_model(llmType, schema, promptResult.data)

        if not runResult.success:
            raise Exception(f"${llmType} 모델 실행 실패: {runResult.message}")

        return success_response(
            message="모델 실행 성공",
            data=schema.parse_raw(runResult.data),
        )
    except Exception as e:
        print(
            "[ERROR] app/services/llm/model.py - run_model_and_format_result 예외 발생:",
            e,
        )

        traceback.print_exc()

        return error_response(
            message="모델 실행 실패",
        )
