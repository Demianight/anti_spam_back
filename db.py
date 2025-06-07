from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "postgresql+psycopg://xc:mypassword@10.10.127.2:5432/messages"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
