from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from messages.crud import (
    create_message,
    get_message_by_id,
    get_unprocessed_messages,
    process_message,
)
from messages.models import Message
from users.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="/messages")


@router.post("/", response_model=Message)
def create_msg(
    msg: Message,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_msg = get_message_by_id(session, msg.message_id)
    if db_msg:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(session, msg)


@router.get("/unprocessed", response_model=list[Message])
def get_unproc(session: Session = Depends(get_session)):
    return get_unprocessed_messages(session)


@router.post("/{message_id}/process", response_model=Message)
def process(message_id: int, session: Session = Depends(get_session)):
    return process_message(session, message_id)


@router.get("/{message_id}", response_model=Message)
def get_msg(message_id: int, session: Session = Depends(get_session)):
    msg = get_message_by_id(session, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
