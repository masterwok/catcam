from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Annotated
from auth import oauth2_scheme
from enum import Enum
from gpio import servo_run_for_seconds


router = APIRouter(prefix="/api", tags=["feed"])


@router.post("/feed")
async def move(req: Request, _token: Annotated[str, Depends(oauth2_scheme)]):
    await servo_run_for_seconds(req.app, 1.0, speed=0.5, direction=1)

    return None
