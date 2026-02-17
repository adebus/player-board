from sqlmodel import Field, SQLModel


class GameOwnerBase(SQLModel):
    game_id: int = Field(foreign_key="game.id")
    owner_id: int = Field(foreign_key="player.id")


class GameOwner(GameOwnerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class GameOwnerCreate(GameOwnerBase):
    pass


class GameOwnerRead(GameOwnerBase):
    id: int
