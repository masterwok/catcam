from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from typing import Annotated
from auth import oauth2_scheme
from enum import Enum
from network import connect_ssid, is_ap_mode
from cmd import run_cmd
from gpio import led_off
from auth import write_credentials


router = APIRouter(prefix="/api", tags=["setup"])

class SetupRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)
    networkName: str = Field(min_length=1, max_length=32)
    networkPassword: str = Field(min_length=0, max_length=128)

@router.post("/setup")
async def setup(req: SetupRequest, request: Request):
    await connect_ssid(req.networkName, req.networkPassword)

    write_credentials(req.username, req.password)

    led_off(request.app)

    return None

@router.get("/setup")
async def setup():
    is_setup = not (await is_ap_mode())

    return { "isSetupComplete": is_setup }
