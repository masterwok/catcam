from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from auth import authenticate_user, create_access_token, Token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    req: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if not authenticate_user(req.username, req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token({"sub": req.username})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,     # JS cannot read it
        secure=False,      # True in production (HTTPS only)
        samesite="lax",    # Lax = safe default, Strict is stronger
        max_age=3600,      # 1 hour
        path="/"           # send cookie on all routes
    )

    return Token(access_token=access_token)