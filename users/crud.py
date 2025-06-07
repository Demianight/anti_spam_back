from sqlmodel import Session, select

from .auth import get_password_hash
from .models import User


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def create_user(session: Session, email: str, password: str) -> User:
    user = User(email=email, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
