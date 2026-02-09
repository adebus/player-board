
from fastapi import FastAPI

from src.models import Game

app = FastAPI()
games: list[Game] = []


@app.post("/games")
def post_game(game: Game) -> dict[str, str | Game]:
    games.append(game)
    return {"message": "Success", "game": games[-1]}


@app.get("/games")
def read_all_games() -> dict[str, list[Game]]:
    return {"games": games}
