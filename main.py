from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse
from routers import auth_router, camera_router, gimbal_router, setup_router
from pathlib import Path
from network import is_ap_mode, start_captive_portal
from gpio import init_gpio
import asyncio

app = FastAPI()

init_gpio(app, asyncio.get_running_loop())

app.mount("/assets", StaticFiles(directory="web/app/dist/assets", html=True), name="assets")
app.mount("/fonts", StaticFiles(directory="web/app/dist/fonts", html=True), name="fonts")

@app.get("/")
async def root():
    return FileResponse(Path("web/app/dist/index.html"))

app.include_router(auth_router.router)
app.include_router(camera_router.router)
app.include_router(gimbal_router.router)
app.include_router(setup_router.router)

# -----------------------
# Primary portal endpoint
# -----------------------

@app.get("/")
@app.get("/portal")

# ---------- Android (AOSP / Chrome) ----------
@app.get("/generate_204")
@app.get("/gen_204")
@app.get("/connectivitycheck.gstatic.com/generate_204")
@app.get("/clients3.google.com/generate_204")

# ---------- Apple (iOS / macOS) ----------
@app.get("/hotspot-detect.html")
@app.get("/library/test/success.html")

# ---------- Windows (NCSI) ----------
@app.get("/ncsi.txt")
@app.get("/connecttest.txt")

# ---------- Firefox (current) ----------
# Host: detectportal.firefox.com
@app.get("/canonical.html")
async def root():
    return RedirectResponse("/", status_code=302)
