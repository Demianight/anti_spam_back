from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    message_id: int = Field(primary_key=True)
    date: int
    chat_id: int | None = None
    chat_type: str | None = None
    user_id: int | None = None
    user_username: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    text: str | None = None
    reply_to_message_id: int | None = None

    spam_score: float
