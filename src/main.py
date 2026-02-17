from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from .database import create_db_and_tables
from .models import game, gameowner, player  # noqa: F401
from .routers import games, players


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(games.router)
app.include_router(players.router)
