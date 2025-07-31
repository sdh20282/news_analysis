from fastapi import APIRouter, UploadFile, File

import traceback

from app.services.api.handle_upload import validate_and_save_excel
from app.schemas.json_response import JSONResponse
from app.utils.response import success_response, error_response


router = APIRouter()


@router.post("/excel", response_model=JSONResponse[None])
async def excel_upload(file: UploadFile = File(...)):
    try:
        if not file:
            raise Exception("파일이 업로드되지 않았습니다.")

        uploadResult = await validate_and_save_excel(file)

        if not uploadResult.success:
            raise Exception(uploadResult.message)

        return success_response(
            message="엑셀 업로드 성공",
        )
    except Exception as e:
        print("[ERROR] app/routes/api/puload.py 예외 발생:", e)
        print(f"File: {file.filename if file else 'No file'}")

        traceback.print_exc()

        return error_response(
            message="엑셀 업로드 실패",
        )
