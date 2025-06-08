from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from messages.crud import (
    create_message,
    filter_messages_by_chat_id,
    get_message_by_id,
    get_unique_chat_ids,
    get_unprocessed_messages,
    process_message,
)
from messages.models import Message
from users.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="/messages")


@router.post("/", response_model=Message)
def create_message_route(
    msg: Message,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_msg = get_message_by_id(session, msg.message_id)
    if db_msg:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(session, msg)


@router.get("/unprocessed", response_model=list[Message])
def get_unprocessed_route(
    chat_id: int | None = None,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if chat_id is not None:
        return filter_messages_by_chat_id(session, chat_id)
    return get_unprocessed_messages(session)


@router.post("/{message_id}/process", response_model=Message)
def process_route(
    message_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return process_message(session, message_id)


@router.get("/unique_chat_ids", response_model=list[int])
def get_unique_chat_ids_route(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_unique_chat_ids(session)
