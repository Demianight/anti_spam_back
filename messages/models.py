from sqlmodel import BigInteger, Column, Field, SQLModel


class Message(SQLModel, table=True):
    message_id: int = Field(primary_key=True)

    chat_id: int | None = Field(sa_column=Column(BigInteger()))
    user_id: int | None = Field(sa_column=Column(BigInteger()))
    reply_to_message_id: int | None = Field(sa_column=Column(BigInteger()))

    date: int
    chat_type: str | None = None
    user_username: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    text: str | None = None

    is_processed: bool | None = False

    spam_score: float
