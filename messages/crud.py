from typing import Sequence

from sqlmodel import Session, select

from messages.models import Message


def create_message(session: Session, message: Message) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_message_by_id(session: Session, message_id: int) -> Message | None:
    return session.get(Message, message_id)


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
    return session.exec(select(Message).where(Message.is_proccesed != True)).all()


def process_message(session: Session, message_id: int):
    message = get_message_by_id(session, message_id)
    if not message:
        return None
    message.is_proccesed = True
    session.add(message)
    session.commit()
    return message
