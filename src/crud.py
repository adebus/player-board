from collections.abc import Sequence

from sqlmodel import Session, select

from src.models import (
    Game,
    GameCreate,
    GameOwner,
    Player,
    PlayerCreate,
)


def create_player(session: Session, player: PlayerCreate) -> Player:

    db_player = Player.model_validate(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


def get_player_by_username(session: Session, username: str) -> Player | None:
    statement = select(Player).where(Player.username == username)
    return session.exec(statement).first()


def get_all_players(session: Session) -> Sequence[Player] | None:
    statement = select(Player)
    return session.exec(statement).all()


def get_game_by_name(session: Session, name: str) -> Game | None:
    statement = select(Game).where(Game.name == name)
    return session.exec(statement).first()


def get_all_games(session: Session) -> Sequence[Game] | None:
    statement = select(Game)
    return session.exec(statement).all()


def create_game(session: Session, game: GameCreate) -> Game:
    db_game = Game.model_validate(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


def create_game_owner(session: Session, game_id: int, player_id: int) -> GameOwner:

    db_game_owner = GameOwner(game_id=game_id, owner_id=player_id)
    session.add(db_game_owner)
    session.commit()
    session.refresh(db_game_owner)
    return db_game_owner


def check_game_owner_exists(session: Session, owner_id: int, game_id: int) -> bool:
    statement = (
        select(GameOwner).where(GameOwner.owner_id == owner_id).where(GameOwner.game_id == game_id)
    )
    return session.exec(statement).first() is not None


def get_game_owners(session: Session, game_id: int) -> Sequence[Player]:
    statement = (
        select(Player)
        .join(GameOwner, GameOwner.owner_id == Player.id)  # type: ignore[arg-type]
        .where(GameOwner.game_id == game_id)
    )
    return session.exec(statement).all()


def get_games_by_owner(session: Session, player_id: int) -> Sequence[Game]:
    statement = (
        select(Game)
        .join(GameOwner, GameOwner.game_id == Game.id)  # type: ignore[arg-type]
        .where(GameOwner.owner_id == player_id)
    )
    return session.exec(statement).all()
