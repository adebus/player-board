from datetime import datetime
from typing import Self

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class GameSessionBase(SQLModel):
    start_time: datetime | None = Field(default=None)
    location: str = Field(min_length=1, max_length=200)
    notes: str | None = Field(max_length=500)


class GameSession(GameSessionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameSessionCreate(GameSessionBase):
    pass


class GameSessionRead(GameSessionBase):
    id: int


class GameSessionPlayerBase(SQLModel):
    game_session_id: int = Field(foreign_key="gamesession.id")
    player_id: int = Field(foreign_key="player.id")


class GameSessionPlayer(GameSessionPlayerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameSessionPlayerCreate(GameSessionPlayerBase):
    pass


class GameSessionPlayerRead(GameSessionPlayerBase):
    id: int


class GamePlayedInSessionBase(SQLModel):
    session_id: int = Field(foreign_key="gamesession.id")
    game_id: int = Field(foreign_key="game.id")
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    notes: str | None = Field(max_length=500)

    @model_validator(mode="after")
    def time_validation(self) -> Self:
        if self.start_time and self.end_time and self.end_time < self.start_time:
            raise ValueError("The end time must be after the start time")
        return self


class GamePlayedInSession(GamePlayedInSessionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GamePlayedInSessionCreate(GamePlayedInSessionBase):
    pass


class GamePlayedInSessionRead(GamePlayedInSessionBase):
    id: int


class GameScoreBase(SQLModel):
    game_played_id: int = Field(foreign_key="gameplayedinsession.id")
    player_id: int = Field(foreign_key="player.id")
    score: int | None = Field(default=None)
    winner: bool = Field(default=False)


class GameScore(GameScoreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameScoreCreate(GameScoreBase):
    pass


class GameScoreRead(GameScoreBase):
    id: int
