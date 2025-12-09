from fastapi import APIRouter, Body
from pydantic import BaseModel
from auth import get_current_user
from gimbal_controller import GimbalController
from enum import Enum


router = APIRouter(prefix="/api", tags=["gimbal"])
gimbal = GimbalController()

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class MoveRequest(BaseModel):
    direction: Direction

@router.post("/move")
async def move(req: MoveRequest, user: str = Depends(get_current_user)):
    match req.direction:
        case Direction.UP:
            gimbal.move_up()
        case Direction.DOWN:
            gimbal.move_down()
        case Direction.LEFT:
            gimbal.move_left()
        case Direction.RIGHT:
            gimbal.move_right()
        case _:
            raise ValueError("Invalid direction")

    return None
