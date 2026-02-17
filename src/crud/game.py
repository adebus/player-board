from collections.abc import Sequence

from sqlmodel import Session, select

from ..models import game as model_game
from ..models import player as model_player


def get_game_by_name(session: Session, name: str) -> model_game.Game | None:
    statement = select(model_game.Game).where(model_game.Game.name == name)
    return session.exec(statement).first()


def get_all_games(session: Session) -> Sequence[model_game.Game] | None:
    statement = select(model_game.Game)
    return session.exec(statement).all()


def create_game(session: Session, game_in: model_game.GameCreate) -> model_game.Game:
    db_game = model_game.Game.model_validate(game_in)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


def create_game_owner(session: Session, game_id: int, player_id: int) -> model_game.GameOwner:

    db_game_owner = model_game.GameOwner(game_id=game_id, owner_id=player_id)
    session.add(db_game_owner)
    session.commit()
    session.refresh(db_game_owner)
    return db_game_owner


def check_game_owner_exists(session: Session, owner_id: int, game_id: int) -> bool:
    statement = (
        select(model_game.GameOwner)
        .where(model_game.GameOwner.owner_id == owner_id)
        .where(model_game.GameOwner.game_id == game_id)
    )
    return session.exec(statement).first() is not None


def get_game_owners(session: Session, game_id: int) -> Sequence[model_player.Player]:
    statement = (
        select(model_player.Player)
        .join(model_game.GameOwner, model_game.GameOwner.owner_id == model_player.Player.id)  # type: ignore[arg-type]
        .where(model_game.GameOwner.game_id == game_id)
    )
    return session.exec(statement).all()


def get_games_by_owner(session: Session, player_id: int) -> Sequence[model_game.Game]:
    statement = (
        select(model_game.Game)
        .join(model_game.GameOwner, model_game.GameOwner.game_id == model_game.Game.id)  # type: ignore[arg-type]
        .where(model_game.GameOwner.owner_id == player_id)
    )
    return session.exec(statement).all()
