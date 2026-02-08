from pydantic import BaseModel


class Game(BaseModel):
    name: str
    min_players: int
    max_players: int
