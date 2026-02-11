from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from src.models import Game, Player

app = FastAPI()

games: list[Game] = []
players: list[Player] = []


@app.post("/games", status_code=201)
def post_game(game: Game) -> dict[str, str | Game]:
    if not any(game.owner == p.username for p in players):
        raise HTTPException(status_code=409, detail="Owner does not exist in the database")
    if any(game.name == g.name and game.owner == g.owner for g in games):
        raise HTTPException(status_code=409, detail="Game already exists for this owner.")
    games.append(game)
    return {"message": "success", "game": games[-1]}


@app.get("/games")
def read_all_games() -> dict[str, str | list[Game]]:
    return {"message": "success", "games": games}


@app.get("/games/{owner}/{name}")
def get_game_by_owner(
    owner: Annotated[str, Path(title="The owner name of the game to find")],
    name: Annotated[str, Path(title="The name of the game to find")],
) -> dict[str, str | Game]:
    for g in games:
        if g.owner == owner and g.name == name:
            return {"message": "success", "game": g}
    raise HTTPException(status_code=404, detail="Game not found")


@app.post("/player", status_code=201)
def post_player(player: Player) -> dict[str, str | Player]:
    if any(p.username == player.username for p in players):
        raise HTTPException(status_code=409, detail="This player already exists")
    players.append(player)
    return {"message": "success", "player": players[-1]}


@app.get("/players")
def get_all_players() -> dict[str, str | list[Player]]:
    return {"message": "success", "players": players}


@app.get("/player/{username}")
def get_player_by_username(
    username: Annotated[str, Path(title="The username of the player to find")],
) -> dict[str, str | Player]:
    for p in players:
        if p.username == username:
            return {"message": "success", "player": p}
    raise HTTPException(status_code=404, detail="Player not found")
