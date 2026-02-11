from pydantic import BaseModel, Field, model_validator


class Game(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    min_players: int = Field(ge=1)
    max_players: int = Field(ge=1, le=10)
    owner: str = Field(min_length=1, max_length=25)

    @model_validator(mode="after")
    def check_player_counts(self) -> Game:
        if self.min_players > self.max_players:
            raise ValueError("Minimum players must be less than or equal to max players")
        return self


class Player(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: str = Field(min_length=4, max_length=50)
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
