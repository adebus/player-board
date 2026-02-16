from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "player_board.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}

db_engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(db_engine)


def get_session() -> Generator[Session]:
    with Session(db_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
