from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from messages.crud import (
    create_message,
    filter_messages_by_chat_id,
    get_message_by_id,
    get_unique_chat_ids,
    get_unprocessed_messages,
    get_user_spam_summary,
    process_message,
)
from messages.models import Message
from users.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="/messages")


@router.post("/", response_model=Message)
def create_message_route(
    msg: Message,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    db_msg = get_message_by_id(session, msg.message_id)
    if db_msg:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(session, msg)


@router.get("/unprocessed", response_model=list[Message])
def get_unprocessed_route(
    chat_id: int | None = None,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    if chat_id is not None:
        return filter_messages_by_chat_id(session, chat_id)
    return get_unprocessed_messages(session)


@router.post("/{chat_id}/{message_id}/process", response_model=Message)
def process_route(
    chat_id: int,
    message_id: int,
    is_spam: bool = False,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return process_message(session, chat_id, message_id, is_spam)


@router.get("/unique_chat_ids", response_model=list[int])
def get_unique_chat_ids_route(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return get_unique_chat_ids(session)


@router.get("/user_spam_summary", response_model=list[dict[str, Any]])
def get_user_spam_summary_route(
    last_n: int = 5,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    return get_user_spam_summary(session, last_n=last_n)
