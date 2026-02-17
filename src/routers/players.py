from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from ..crud import game as crud_game
from ..crud import player as crud_player
from ..database import SessionDep
from ..models import player as model_player

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", status_code=201, response_model=model_player.PlayerRead)
def post_player(
    session: SessionDep, player_in: model_player.PlayerCreate
) -> model_player.PlayerRead:
    existing = crud_player.get_player_by_username(session, player_in.username)

    if existing:
        raise HTTPException(status_code=409, detail="This player already exists")

    new_player = crud_player.create_player(session, player_in)

    return model_player.PlayerRead(**new_player.model_dump(), games=[])


@router.get("/", response_model=list[model_player.PlayerRead])
def get_all_players(session: SessionDep) -> Sequence[model_player.PlayerRead] | None:
    all_players = crud_player.get_all_players(session)

    if not all_players:
        return []

    all_players_with_games: list[model_player.PlayerRead] = []

    for p in all_players:
        assert p.id is not None

        games = crud_game.get_games_by_owner(session, p.id)

        all_players_with_games.append(
            model_player.PlayerRead(**p.model_dump(), games=[g.name for g in games])
        )

    return all_players_with_games


@router.get("/{username}", response_model=model_player.PlayerRead)
def get_player_by_username(
    session: SessionDep,
    username: Annotated[str, Path(title="The username of the player to find")],
) -> model_player.PlayerRead:
    response = crud_player.get_player_by_username(session, username)

    if not response:
        raise HTTPException(status_code=404, detail="Player not found")

    assert response.id is not None

    games = crud_game.get_games_by_owner(session, response.id)

    return model_player.PlayerRead(
        **response.model_dump(),
        games=[g.name for g in games],
    )
