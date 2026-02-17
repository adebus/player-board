from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from ..crud import game as crud_game
from ..crud import player as crud_player
from ..database import SessionDep
from ..models import game as model_game

router = APIRouter(prefix="/games", tags=['games'])


@router.post("/", status_code=201, response_model=model_game.GameRead)
def post_game(session: SessionDep, game_in: model_game.GameCreate) -> model_game.GameRead:
    db_player = crud_player.get_player_by_username(session, game_in.owner)
    if not db_player:
        raise HTTPException(status_code=404, detail="Owner does not exist in the database")

    assert db_player.id is not None

    db_game = crud_game.get_game_by_name(session, game_in.name)
    if db_game:
        assert db_game.id is not None
        if crud_game.check_game_owner_exists(session, db_player.id, db_game.id):
            raise HTTPException(status_code=409, detail="Game already exists for this owner.")

    if not db_game:
        db_game = crud_game.create_game(session, game_in)

    assert db_game.id is not None

    crud_game.create_game_owner(session, db_game.id, db_player.id)

    owners = crud_game.get_game_owners(session, db_game.id)
    return model_game.GameRead(**db_game.model_dump(), owners=[p.username for p in owners])


@router.get("/", response_model=list[model_game.GameRead])
def read_all_games(session: SessionDep) -> Sequence[model_game.GameRead] | None:
    all_games = crud_game.get_all_games(session)

    if not all_games:
        return []

    all_games_with_owners: list[model_game.GameRead] = []

    for g in all_games:
        assert g.id is not None

        owners = crud_game.get_game_owners(session, g.id)

        all_games_with_owners.append(
            model_game.GameRead(**g.model_dump(), owners=[p.username for p in owners])
        )

    return all_games_with_owners


@router.get("/{owner}/{name}", response_model=model_game.GameRead)
def get_game_by_owner(
    session: SessionDep,
    owner: Annotated[str, Path(title="The owner name of the game to find")],
    name: Annotated[str, Path(title="The name of the game to find")],
) -> model_game.GameRead:
    db_player = crud_player.get_player_by_username(session, owner)

    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    assert db_player.id is not None

    db_game = crud_game.get_game_by_name(session, name)

    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    assert db_game.id is not None

    game_owner = crud_game.check_game_owner_exists(session, db_player.id, db_game.id)

    if not game_owner:
        raise HTTPException(status_code=404, detail="Game not owned by owner")

    owners = crud_game.get_game_owners(session, db_game.id)
    return model_game.GameRead(**db_game.model_dump(), owners=[p.username for p in owners])
