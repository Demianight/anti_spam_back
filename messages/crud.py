from collections import defaultdict
from typing import Any, Sequence

from sqlmodel import Session, select

from messages.models import Message
from messages.producer import send_message_to_kafka


def create_message(session: Session, message: Message) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_message_by_id(session: Session, message_id: int) -> Message | None:
    return session.get(Message, message_id)


def get_message_by_id_and_chat_id(
    session: Session, chat_id: int, message_id: int
) -> Message | None:
    return session.exec(
        select(Message).filter(
            (Message.chat_id == chat_id) & (Message.message_id == message_id)
        )
    ).first()


def get_all_messages(session: Session) -> Sequence[Message]:
    return session.exec(select(Message)).all()


def delete_message(session: Session, message_id: int) -> bool:
    message = session.get(Message, message_id)
    if message:
        session.delete(message)
        session.commit()
        return True
    return False


def update_message(session: Session, message_id: int, **kwargs) -> Message | None:
    message = session.get(Message, message_id)
    if not message:
        return None

    for key, value in kwargs.items():
        if hasattr(message, key):
            setattr(message, key, value)

    session.commit()
    session.refresh(message)
    return message


def get_unprocessed_messages(session: Session) -> Sequence[Message]:
    return session.exec(
        select(Message).where(
            (Message.is_processed == None) | (Message.is_processed == False)
        )
    ).all()


async def process_message(
    session: Session, chat_id: int, message_id: int, is_spam: bool
):
    message = get_message_by_id_and_chat_id(session, chat_id, message_id)
    if not message:
        return None
    if is_spam:
        await send_message_to_kafka(message.model_dump())
    message.is_processed = True
    session.add(message)
    session.commit()

    return message


def filter_messages_by_chat_id(session: Session, chat_id: int) -> Sequence[Message]:
    return session.exec(select(Message).where(Message.chat_id == chat_id)).all()


def get_unique_chat_ids(session: Session) -> Sequence[int | None]:
    return session.exec(select(Message.chat_id).distinct()).all()


def get_user_spam_summary(session: Session, last_n: int = 5) -> list[dict[str, Any]]:
    # Get all messages ordered by user_id and descending date
    statement = select(Message).order_by(Message.user_id, Message.date.desc())
    messages = session.exec(statement).all()

    user_data = defaultdict(
        lambda: {"username": None, "spam_score": 0.0, "last_messages": []}
    )

    for msg in messages:
        data = user_data[msg.user_id]
        data["username"] = msg.user_username
        data["spam_score"] += msg.spam_score
        if len(data["last_messages"]) < last_n:
            data["last_messages"].append(msg.text)

    return list(user_data.values())
