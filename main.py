from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth_router, camera_router, gimbal_router
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
async def root():
    return FileResponse(Path("web/app/index.html"))

app.include_router(auth_router.router)
app.include_router(gimbal_router.router)
app.include_router(camera_router.router)
