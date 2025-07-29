from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("", response_class=HTMLResponse)
async def extract(request: Request):
    return templates.TemplateResponse(
        "ui/extract.html",
        {
            "request": request,
        }
    )