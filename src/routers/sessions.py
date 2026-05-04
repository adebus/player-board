from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from ..crud import session as crud_session
from ..database import SessionDep
from ..models import session as model_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


# POST /sessions
# Inputs: start_time, location, notes?, [players]?
# Returns: GameSesionRead
# Validation: any players provided must exist
# Notes: In future when account feature is live, presume the person creating the session is attending, which will make [players] optional
@router.post("/", status_code=201, response_model=model_session.GameSessionRead)
def post_game_session(
    session: SessionDep, game_session_in: model_session.GameSessionCreate
) -> model_session.GameSessionRead:

    # player_ids: list[int] = []
    # for p in players:
    #     db_player = crud_player.get_player_by_username(session, p)
    #     if not db_player:
    #         # TODO: In the future I want to change this to return an indivdual error that the player wasn't found, not just bomb the whole process out.
    #         raise HTTPException(status_code=404, detail=f"Player {p} does not exist in the database")
    #     player_ids.append(db_player.id)

    db_game_session = crud_session.create_game_session(session, game_session_in)

    # assert db_game_session.id is not None

    # for p in player_ids:
    #     crud_session.add_player_to_session(session, db_game_session.id, p)

    return model_session.GameSessionRead(**db_game_session.model_dump())


# GET /sessions
# Inputs: none
# Returns: [GameSessionRead]
# Validation: none
@router.get("/", response_model=list[model_session.GameSessionRead])
def get_all_game_sessions(session: SessionDep) -> Sequence[model_session.GameSessionRead]:
    all_game_sessions = crud_session.get_all_game_sessions(session)

    if not all_game_sessions:
        return []

    all_gs: list[model_session.GameSessionRead] = []
    for gs in all_game_sessions:
        assert gs.id is not None
        all_gs.append(model_session.GameSessionRead(**gs.model_dump()))

    return all_gs


# GET /sessions/{id}
# Inputs: id
# Returns: GameSessionRead
# Validation: none
@router.get("/{id}", response_model=model_session.GameSessionRead)
def get_game_session_by_id(
    session: SessionDep, id: Annotated[int, Path(title="The id of the session to get")]
) -> model_session.GameSessionRead:
    db_game_session = crud_session.get_game_session_by_id(session, id)
    if not db_game_session:
        raise HTTPException(status_code=404, detail="Game Session Not Found")

    return model_session.GameSessionRead(**db_game_session.model_dump())


# POST /sessions/players
# Inputs: [GameSessionPlayerCreate]
# Returns: [GameSessionPlayerRead]
# Validation: any players provided must exist
@router.post("/players", status_code=201, response_model=model_session.GameSessionPlayerRead)
def post_session_player(
    session: SessionDep, game_session_player_in: model_session.GameSessionPlayerCreate
) -> model_session.GameSessionPlayerRead:

    added_player = crud_session.add_player_to_session(session, game_session_player_in)

    return model_session.GameSessionPlayerRead(**added_player.model_dump())


# GET /sessions/{id}/players
# input: id
# Returns: [PlayerRead]
# Validation: none

# POST /sessions/{id}/games
# Input: id, [game_id, start_time?, end_time?, notes?]
# Returns: [GameRead]
# Validation: any games must be in the games table.

# GET /sessions/{id}/games
# Input: id
# Returns: [GameRead]
# Validation: none

# GET /sessions/{id}/games/{game_played_id}
# Input: id, game_played_id
# Returns: [GameRead]
# Validation: none

# POST /sessions/{id}/games/{game_id}/scores
# Input: id, game_id, [player_id, score?, winner?]
# Returns: [GameScoreRead]
# Validation: game must be played in session, players must exist in session

# GET /sessions/{id}/games/{game_id}/scores
# Input: id, game_id
# Returns [GameScoreRead]
# Validation: none

# GET /sessions/{id}/games/{game_id}/scores/{player_id}
# Input: id, game_id, player_id
# Returns: GameScoreRead
# Validation: none
