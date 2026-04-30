from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.ask import router as ask_router
from app.routes.feedback import router as feedback_router
from app.routes.health import router as health_router
from app.routes.sources import router as sources_router
from app.version import APP_VERSION

BASE_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = BASE_DIR / "web"

app = FastAPI(
    title="Parenting KB V1",
    description="面向 0-3 岁家庭场景的基础育儿助手原型",
    version=APP_VERSION,
)

app.include_router(health_router)
app.include_router(ask_router)
app.include_router(sources_router)
app.include_router(feedback_router)

if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")


@app.get("/")
def root():
    index_path = WEB_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    return {
        "name": "parenting_kb_v1",
        "message": "service is running",
        "docs": "/docs",
    }
