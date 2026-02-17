from collections.abc import Sequence

from sqlmodel import Session, select

from ..models import player


def create_player(session: Session, player_in: player.PlayerCreate) -> player.Player:

    db_player = player.Player.model_validate(player_in)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


def get_player_by_username(session: Session, username: str) -> player.Player | None:
    statement = select(player.Player).where(player.Player.username == username)
    return session.exec(statement).first()


def get_all_players(session: Session) -> Sequence[player.Player] | None:
    statement = select(player.Player)
    return session.exec(statement).all()
