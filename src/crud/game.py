from collections.abc import Sequence

from sqlmodel import Session, select

from ..models import game, gameowner, player


def get_game_by_name(session: Session, name: str) -> game.Game | None:
    statement = select(game.Game).where(game.Game.name == name)
    return session.exec(statement).first()


def get_all_games(session: Session) -> Sequence[game.Game] | None:
    statement = select(game.Game)
    return session.exec(statement).all()


def create_game(session: Session, game_in: game.GameCreate) -> game.Game:
    db_game = game.Game.model_validate(game_in)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


def create_game_owner(session: Session, game_id: int, player_id: int) -> gameowner.GameOwner:

    db_game_owner = gameowner.GameOwner(game_id=game_id, owner_id=player_id)
    session.add(db_game_owner)
    session.commit()
    session.refresh(db_game_owner)
    return db_game_owner


def check_game_owner_exists(session: Session, owner_id: int, game_id: int) -> bool:
    statement = (
        select(gameowner.GameOwner)
        .where(gameowner.GameOwner.owner_id == owner_id)
        .where(gameowner.GameOwner.game_id == game_id)
    )
    return session.exec(statement).first() is not None


def get_game_owners(session: Session, game_id: int) -> Sequence[player.Player]:
    statement = (
        select(player.Player)
        .join(gameowner.GameOwner, gameowner.GameOwner.owner_id == player.Player.id)  # type: ignore[arg-type]
        .where(gameowner.GameOwner.game_id == game_id)
    )
    return session.exec(statement).all()


def get_games_by_owner(session: Session, player_id: int) -> Sequence[game.Game]:
    statement = (
        select(game.Game)
        .join(gameowner.GameOwner, gameowner.GameOwner.game_id == game.Game.id)  # type: ignore[arg-type]
        .where(gameowner.GameOwner.owner_id == player_id)
    )
    return session.exec(statement).all()
