from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from messages.crud import create_message, get_message_by_id
from messages.models import Message

router = APIRouter(prefix="/messages")


@router.post("/", response_model=Message)
def create_msg(msg: Message, session: Session = Depends(get_session)):
    db_msg = get_message_by_id(session, msg.message_id)
    if db_msg:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(session, msg)


@router.get("/{message_id}", response_model=Message)
def get_msg(message_id: int, session: Session = Depends(get_session)):
    msg = get_message_by_id(session, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
