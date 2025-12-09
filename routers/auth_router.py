from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated

from auth import authenticate_user, create_access_token, Token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(req: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not authenticate_user(req.username, req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token({"sub": req.username})

    return Token(access_token=access_token)