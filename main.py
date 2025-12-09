from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth_router, camera_router, gimbal_router
from pathlib import Path

app = FastAPI()

# TODO (JT): REMOVE AFTER FE DEV IS DONE
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],        # allow all domains
#    allow_credentials=True,
#    allow_methods=["*"],        # allow all HTTP methods
#    allow_headers=["*"],        # allow all request headers
#)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.2:5173", "http://localhost:5173"],  # exact origin of your SPA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
async def root():
    return FileResponse(Path("web/index.html"))

app.include_router(auth_router.router)
app.include_router(gimbal_router.router)
app.include_router(camera_router.router)
