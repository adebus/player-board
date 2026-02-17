from typing import Self

from pydantic import EmailStr, model_validator
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


class PlayerBase(SQLModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr = Field(min_length=4, max_length=50)
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)


class Player(PlayerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    id: int
    games: list[str] = []


class GameOwnerBase(SQLModel):
    game_id: int = Field(foreign_key="game.id")
    owner_id: int = Field(foreign_key="player.id")


class GameOwner(GameOwnerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameOwnerCreate(GameOwnerBase):
    pass


class GameOwnerRead(GameOwnerBase):
    id: int
