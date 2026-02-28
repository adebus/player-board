from collections.abc import Sequence

from sqlmodel import Session, select

from ..models import game as model_game
from ..models import player as model_player
from ..models import session as model_session


def create_game_session(
    session: Session, game_session: model_session.GameSessionCreate
) -> model_session.GameSession:
    db_game_session = model_session.GameSession.model_validate(game_session)
    session.add(db_game_session)
    session.commit()
    session.refresh(db_game_session)
    return db_game_session


def get_game_session_by_id(
    session: Session, game_session_id: int
) -> model_session.GameSession | None:
    statement = select(model_session.GameSession).where(
        model_session.GameSession.id == game_session_id
    )

    return session.exec(statement).first()


def get_all_game_sessions(session: Session) -> Sequence[model_session.GameSession] | None:
    statement = select(model_session.GameSession)

    return session.exec(statement).all()


# def update_game_session_by_id(
#     session: Session, game_session_id: int, updates: dict[str, Any]
# ) -> model_session.GameSession | None:
#     statement = select(model_session.GameSession).where(
#         model_session.GameSession.id == game_session_id
#     )

#     game_session = session.exec(statement).first()

#     if not game_session:
#         return None

#     if updates["start_time"]:
#         game_session.start_time = updates["start_time"]

#     if updates["location"]:
#         game_session.location = updates["location"]

#     if updates["notes"]:
#         game_session.notes = updates["notes"]

#     session.add(game_session)

#     session.commit()
#     session.refresh(game_session)

#     return game_session


# def remove_game_session_by_id(
#     session: Session, game_session_id: int
# ) -> model_session.GameSession | None:
#     statement = select(model_session.GameSession).where(
#         model_session.GameSession.id == game_session_id
#     )

#     game_session = session.exec(statement).first()

#     if not game_session:
#         return None

#     session.delete(game_session)
#     session.commit()

#     return game_session


def add_player_to_session(
    session: Session, game_session_id: int, player_id: int
) -> model_session.GameSessionPlayer:

    db_game_session_player = model_session.GameSessionPlayer.model_validate(
        {"game_session_id": game_session_id, "player_id": player_id}
    )

    session.add(db_game_session_player)
    session.commit()
    session.refresh(db_game_session_player)

    return db_game_session_player


def get_session_players(
    session: Session, game_session_id: int
) -> Sequence[model_player.Player] | None:

    statement2 = (
        select(model_player.Player)
        .join(
            model_session.GameSessionPlayer,
            model_session.GameSessionPlayer.player_id == model_player.Player.id,  # type: ignore[arg-type]
        )
        .where(model_session.GameSessionPlayer.game_session_id == game_session_id)
    )

    return session.exec(statement2).all()


def check_player_in_session(session: Session, game_session_id: int, player_id: int) -> bool:
    statement = (
        select(model_session.GameSessionPlayer)
        .where(model_session.GameSessionPlayer.game_session_id == game_session_id)
        .where(model_session.GameSessionPlayer.player_id == player_id)
    )

    return session.exec(statement).first() is not None


def add_game_played_in_session(
    session: Session, game_session_game: model_session.GamePlayedInSessionCreate
) -> model_session.GamePlayedInSession:

    db_game_played_in_session = model_session.GamePlayedInSession.model_validate(game_session_game)
    session.add(db_game_played_in_session)
    session.commit()
    session.refresh(db_game_played_in_session)

    return db_game_played_in_session


def get_all_games_played_in_session(
    session: Session, game_session_id: int
) -> Sequence[model_game.Game] | None:

    statement2 = (
        select(model_game.Game)
        .join(
            model_session.GamePlayedInSession,
            model_session.GamePlayedInSession.game_id == model_game.Game.id,  # type: ignore[arg-type]
        )
        .where(model_session.GamePlayedInSession.session_id == game_session_id)
    )

    return session.exec(statement2).all()


def add_game_score(
    session: Session, game_score: model_session.GameScoreCreate
) -> model_session.GameScore:
    db_game_score = model_session.GameScore.model_validate(game_score)

    session.add(db_game_score)
    session.commit()
    session.refresh(db_game_score)

    return db_game_score


def get_game_scores(session: Session, game_played_id: int) -> Sequence[model_session.GameScore]:
    statement = (
        select(model_session.GameScore)
        .join(model_player.Player, model_player.Player.id == model_session.GameScore.player_id)  # type: ignore[arg-type]
        .where(model_session.GameScore.game_played_id == game_played_id)
    )

    return session.exec(statement).all()
