from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Annotated
from auth import oauth2_scheme
from enum import Enum
from network import connect_ssid
from cmd import run_cmd


router = APIRouter(prefix="/api", tags=["setup"])

class SetupRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)
    networkName: str = Field(min_length=1, max_length=32)
    networkPassword: str = Field(min_length=0, max_length=128)


@router.post("/setup")
async def setup(req: SetupRequest):
    await connect_ssid(req.networkName, req.networkPassword)

    return None
