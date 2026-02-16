from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import FastAPI, HTTPException, Path

import src.crud as crud
from src.database import SessionDep, create_db_and_tables
from src.models import GameCreate, GameRead, PlayerCreate, PlayerRead


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/games", status_code=201, response_model=GameRead)
def post_game(session: SessionDep, game: GameCreate) -> GameRead:
    player = crud.get_player_by_username(session, game.owner)
    if not player:
        raise HTTPException(status_code=404, detail="Owner does not exist in the database")

    assert player.id is not None

    db_game = crud.get_game_by_name(session, game.name)
    if db_game:
        assert db_game.id is not None
        if crud.check_game_owner_exists(session, player.id, db_game.id):
            raise HTTPException(status_code=409, detail="Game already exists for this owner.")

    if not db_game:
        db_game = crud.create_game(session, game)

    assert db_game.id is not None

    crud.create_game_owner(session, db_game.id, player.id)

    owners = crud.get_game_owners(session, db_game.id)
    return GameRead(**db_game.model_dump(), owners=[p.username for p in owners])


@app.get("/games", response_model=list[GameRead])
def read_all_games(session: SessionDep) -> Sequence[GameRead] | None:
    all_games = crud.get_all_games(session)

    if not all_games:
        return []

    all_games_with_owners: list[GameRead] = []

    for game in all_games:
        assert game.id is not None

        owners = crud.get_game_owners(session, game.id)

        all_games_with_owners.append(
            GameRead(**game.model_dump(), owners=[p.username for p in owners])
        )

    return all_games_with_owners


@app.get("/games/{owner}/{name}", response_model=GameRead)
def get_game_by_owner(
    session: SessionDep,
    owner: Annotated[str, Path(title="The owner name of the game to find")],
    name: Annotated[str, Path(title="The name of the game to find")],
) -> GameRead:
    player = crud.get_player_by_username(session, owner)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    assert player.id is not None

    game = crud.get_game_by_name(session, name)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    assert game.id is not None

    game_owner = crud.check_game_owner_exists(session, player.id, game.id)

    if not game_owner:
        raise HTTPException(status_code=404, detail="Game not owned by owner")

    owners = crud.get_game_owners(session, game.id)
    return GameRead(**game.model_dump(), owners=[p.username for p in owners])


@app.post("/player", status_code=201, response_model=PlayerRead)
def post_player(session: SessionDep, player: PlayerCreate) -> PlayerRead:
    existing = crud.get_player_by_username(session, player.username)

    if existing:
        raise HTTPException(status_code=409, detail="This player already exists")

    new_player = crud.create_player(session, player)

    return PlayerRead(**new_player.model_dump(), games=[])


@app.get("/players", response_model=list[PlayerRead])
def get_all_players(session: SessionDep) -> Sequence[PlayerRead] | None:
    all_players = crud.get_all_players(session)

    if not all_players:
        return []

    all_players_with_games: list[PlayerRead] = []

    for player in all_players:
        assert player.id is not None

        games = crud.get_games_by_owner(session, player.id)

        all_players_with_games.append(
            PlayerRead(**player.model_dump(), games=[g.name for g in games])
        )

    return all_players_with_games


@app.get("/player/{username}", response_model=PlayerRead)
def get_player_by_username(
    session: SessionDep,
    username: Annotated[str, Path(title="The username of the player to find")],
) -> PlayerRead:
    response = crud.get_player_by_username(session, username)

    if not response:
        raise HTTPException(status_code=404, detail="Player not found")

    assert response.id is not None

    games = crud.get_games_by_owner(session, response.id)

    return PlayerRead(
        **response.model_dump(),
        games=[g.name for g in games],
    )
