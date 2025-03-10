from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import router
from app.config import Settings

app = FastAPI(
    title="Tech News Briefing API",
    description="API for personalized tech news briefings with AI summaries",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.include_router(router)

@app.get("/")
async def root():
    return FileResponse("app/static/index.html") 