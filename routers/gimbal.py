from fastapi import APIRouter, Body
from gimbal_controller import GimbalController
from enum import Enum

router = APIRouter(prefix="/api", tags=["gimbal"])
gimbal = GimbalController()

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

@router.post("/move")
async def move(direction: Direction = Body(...)):
    match direction:
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

    return {"direction": direction.value}
