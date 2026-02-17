from typing import Self

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class GameBase(SQLModel):
    name: str = Field(min_length=1, max_length=200)
    min_players: int = Field(ge=1)
    max_players: int = Field(ge=1, le=10)

    @model_validator(mode="after")
    def check_player_counts(self) -> Self:
        if self.min_players > self.max_players:
            raise ValueError("Minimum players must be less than or equal to max players")
        return self


class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameCreate(GameBase):
    owner: str = Field(min_length=4, max_length=20)


class GameRead(GameBase):
    id: int
    owners: list[str] = []
