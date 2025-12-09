from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import gimbal, camera, auth
from pathlib import Path

app = FastAPI()

# TODO (JT): REMOVE AFTER FE DEV IS DONE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all domains
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all request headers
)


app.mount("/static", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
async def root():
    return FileResponse(Path("web/index.html"))

app.include_router(auth.router)
app.include_router(gimbal.router)
app.include_router(camera.router)
