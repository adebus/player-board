from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.main import app, games

client = TestClient(app)


@pytest.fixture
def empty_games() -> Any:
    games.clear()
    return games


def test_post_game(empty_games: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    response = client.post("/games", json=test_game)

    assert response.status_code == 201
    assert response.json() == {"message": "Success", "game": test_game}


def test_post_duplicate_game(empty_games: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    client.post("/games", json=test_game)
    response = client.post("/games", json=test_game)

    assert response.status_code == 409


def test_post_invalid_players(empty_games: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 4,
        "max_players": 1,
        "owner": "Tauvix",
    }

    response = client.post("/games", json=test_game)

    assert response.status_code == 422


def test_get_game_1(empty_games: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    client.post("/games", json=test_game)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == {"games": [test_game]}


def test_get_game_2(empty_games: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == {"games": [test_game_1, test_game_2]}


def test_get_specific_game(empty_games: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games/Tauvix/Gloomhaven")

    assert response.status_code == 200
    assert response.json() == {"game": test_game_2}


def test_get_specific_game_failure(empty_games: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Tauvix",
    }

    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games/Tauvix/Clank")

    assert response.status_code == 404
