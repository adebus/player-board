from pydantic import EmailStr
from sqlmodel import Field, SQLModel


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
