from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    message = "🔥 FastAPI로 구축된 LLM 관리 시스템에 오신 걸 환영합니다!"
    return templates.TemplateResponse(
        "ui/home/index.html",
        {
            "request": request,
            "message": message
        }
    )