from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from src.models import Game

app = FastAPI()
games: list[Game] = []


@app.post("/games", status_code=201)
def post_game(game: Game) -> dict[str, str | Game]:
    if any(game.name == g.name and game.owner == g.owner for g in games):
        raise HTTPException(status_code=409, detail="Game already exists for this owner.")
    games.append(game)
    return {"message": "Success", "game": games[-1]}


@app.get("/games")
def read_all_games() -> dict[str, list[Game]]:
    return {"games": games}


@app.get("/games/{owner}/{name}")
def get_game_by_owner(
    owner: Annotated[str, Path(title="The owner name of the game to find")],
    name: Annotated[str, Path(title="The name of the game to find")],
) -> dict[str, Game]:
    for g in games:
        if g.owner == owner and g.name == name:
            return {"game": g}
    raise HTTPException(status_code=404, detail="Game not found")
