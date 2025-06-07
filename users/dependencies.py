from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session

from db import get_session
from users.crud import get_user_by_email

from .auth import ALGORITHM, SECRET_KEY

BearerToken = HTTPBearer()


def get_current_user(
    session: Session = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(BearerToken),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user
