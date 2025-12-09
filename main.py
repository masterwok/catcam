from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import gimbal, camera
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
async def root():
    return FileResponse(Path("web/index.html"))

app.include_router(gimbal.router)
app.include_router(camera.router)
