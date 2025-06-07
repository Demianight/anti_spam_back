from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from messages import messages_router
from users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(messages_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
