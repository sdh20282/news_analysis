from fastapi import FastAPI, Request
from fastapi.responses import Response, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException as StarletteHTTPException

# routers
from app.routes.ui import router as ui_router
from app.routes.api import router as api_router

app = FastAPI()

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def block_devtools_probe():
    return Response(status_code=204)

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
        return RedirectResponse(url="/home")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# 정적 파일 (CSS, JS 등) 연결
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# UI 템플릿 라우터 (Jinja2 기반)
app.include_router(ui_router)

# API 라우터 전체 (prefix = /api)
app.include_router(api_router, prefix="/api")