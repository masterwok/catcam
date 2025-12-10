from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import auth_router, camera_router, gimbal_router
from pathlib import Path

app = FastAPI()

origins = [
    "http://192.168.1.86:5173",  # Vite dev
    # add "https://192.168.1.86:5173" if you run Vite over HTTPS later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,   # required if you're using cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
async def root():
    return FileResponse(Path("web/app/index.html"))

app.include_router(auth_router.router)
app.include_router(gimbal_router.router)
app.include_router(camera_router.router)
