from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel

from crud import create_message, get_message_by_id
from db import engine, get_session
from models import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup if needed
    # SQLModel.metadata.drop_all(engine)  # Uncomment to drop tables on shutdown


app = FastAPI(lifespan=lifespan)


# Dependency injection
@app.post("/messages/", response_model=Message)
def create_msg(msg: Message, session: Session = Depends(get_session)):
    db_msg = get_message_by_id(session, msg.message_id)
    if db_msg:
        raise HTTPException(status_code=400, detail="Message already exists")
    return create_message(session, msg)


@app.get("/messages/{message_id}", response_model=Message)
def get_msg(message_id: int, session: Session = Depends(get_session)):
    msg = get_message_by_id(session, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
