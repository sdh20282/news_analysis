from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("", response_class=HTMLResponse)
async def compare(request: Request):
    return templates.TemplateResponse(
        "ui/compare.html",
        {
            "request": request,
        }
    )