from fastapi import APIRouter, BackgroundTasks

import subprocess
import traceback
import os

from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response

router = APIRouter()

training_process = None
LOG_PATH = "logs/train.log"
TRAIN_SCRIPT = "scripts/train.py"
INPUT_PATH = "data/uploads/uploaded_data.jsonl"


@router.post("/start")
async def start_finetuning(background_tasks: BackgroundTasks) -> JSONResponse[None]:
    try:
        global training_process

        if training_process and training_process.poll() is None:
            raise Exception("이미 학습이 진행 중입니다.")

        def run_training():
            global training_process

            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

            with open(LOG_PATH, "w", encoding="utf-8") as log_file:
                training_process = subprocess.Popen(
                    ["python", TRAIN_SCRIPT, "--input", INPUT_PATH],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                )

        background_tasks.add_task(run_training)

        return success_response(
            message="파인튜닝이 시작되었습니다. 학습 로그를 확인하세요."
        )
    except Exception as e:
        print("[ERROR] app/routes/api/finetune.py 예외 발생:", e)

        traceback.print_exc()

        return error_response(message="파인튜닝 시작 중 오류가 발생했습니다.")


@router.post("/stop")
async def stop_finetuning() -> JSONResponse[None]:
    try:
        global training_process

        if training_process and training_process.poll() is None:
            training_process.terminate()
            training_process = None

            return success_response(message="파인튜닝이 중단되었습니다.")

        return success_response(message="학습이 진행 중이지 않습니다.")
    except Exception as e:
        print("[ERROR] app/routes/api/finetune.py 예외 발생:", e)
        traceback.print_exc()

        return error_response(message="파인튜닝 중단 중 오류가 발생했습니다.")


@router.get("/logs")
async def get_finetune_logs() -> JSONResponse[str]:
    try:
        if not os.path.exists(LOG_PATH):
            raise FileNotFoundError

        global training_process

        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            logs = f.read()

        return success_response(message=logs)
    except FileNotFoundError:
        return error_response(message="학습 로그 파일이 존재하지 않습니다.")
    except Exception as e:
        print("[ERROR] 로그 파일 읽기 실패:", e)

        traceback.print_exc()

        return error_response(message="학습 로그를 가져오는 중 오류가 발생했습니다.")
