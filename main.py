from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth_router, camera_router, gimbal_router
from pathlib import Path

app = FastAPI()

app.mount("/assets", StaticFiles(directory="web/app/dist/assets", html=True), name="assets")

@app.get("/")
async def root():
    return FileResponse(Path("web/app/dist/index.html"))

app.include_router(auth_router.router)
app.include_router(gimbal_router.router)
app.include_router(camera_router.router)
