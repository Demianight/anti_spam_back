from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db import get_session

from .auth import create_access_token, verify_password
from .crud import create_user, get_user_by_email
from .schemas import Token, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token)
def signup(data: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_email(session, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(session, data.email, data.password)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login(
    form_data: UserCreate,
    session: Session = Depends(get_session),
):
    user = get_user_by_email(session, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
