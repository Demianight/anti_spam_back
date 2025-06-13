from sqlmodel import Session, SQLModel, create_engine

from config import DB_DB, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
)

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
