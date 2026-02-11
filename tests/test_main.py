from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.main import app, games, players

client = TestClient(app)


@pytest.fixture
def empty_games() -> Any:
    games.clear()
    return games


@pytest.fixture
def empty_players() -> Any:
    players.clear()
    return players


def test_post_game(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }

    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    response = client.post("/games", json=test_game)

    assert response.status_code == 201
    assert response.json() == {"message": "success", "game": test_game}


def test_post_game_no_player(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }

    response = client.post("/games", json=test_game)

    assert response.status_code == 409


def test_post_game_no_player_2(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test2",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)

    response = client.post("/games", json=test_game)

    assert response.status_code == 409


def test_post_duplicate_game(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    client.post("/games", json=test_game)
    response = client.post("/games", json=test_game)

    assert response.status_code == 409


def test_post_invalid_players(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 4,
        "max_players": 1,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)

    response = client.post("/games", json=test_game)

    assert response.status_code == 422


def test_get_game_1(empty_games: Any, empty_players: Any) -> None:
    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    client.post("/games", json=test_game)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == {"message": "success", "games": [test_game]}


def test_get_game_2(empty_games: Any, empty_players: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games")

    assert response.status_code == 200
    assert response.json() == {"message": "success", "games": [test_game_1, test_game_2]}


def test_get_specific_game(empty_games: Any, empty_players: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games/Test/Gloomhaven")

    assert response.status_code == 200
    assert response.json() == {"message": "success", "game": test_game_2}


def test_get_specific_game_failure(empty_games: Any, empty_players: Any) -> None:
    test_game_1: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)

    client.post("/games", json=test_game_1)
    client.post("/games", json=test_game_2)

    response = client.get("/games/Tauvix/Clank")

    assert response.status_code == 404


def test_post_players(empty_players: Any, empty_games: Any) -> None:
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    response = client.post("/player", json=test_player)

    assert response.status_code == 201
    assert response.json() == {"message": "success", "player": test_player}


def test_post_duplicate_player(empty_players: Any, empty_games: Any) -> None:
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    client.post("/player", json=test_player)
    response = client.post("/player", json=test_player)

    assert response.status_code == 409


def test_get_all_players(empty_players: Any, empty_games: Any) -> None:
    test_player_1: dict[str, str] = {
        "username": "Test1",
        "email": "test1@test.com",
        "first_name": "First1",
        "last_name": "Last1",
    }
    test_player_2: dict[str, str] = {
        "username": "Test2",
        "email": "test2@test.com",
        "first_name": "First2",
        "last_name": "Last2",
    }

    client.post("/player", json=test_player_1)
    client.post("/player", json=test_player_2)

    response = client.get("/players")

    assert response.status_code == 200
    assert response.json() == {"message": "success", "players": [test_player_1, test_player_2]}


def test_get_player_by_username(empty_players: Any, empty_games: Any) -> None:
    test_player_1: dict[str, str] = {
        "username": "Test1",
        "email": "test1@test.com",
        "first_name": "First1",
        "last_name": "Last1",
    }

    client.post("/player", json=test_player_1)

    response = client.get("/player/Test1")

    assert response.status_code == 200
    assert response.json() == {"message": "success", "player": test_player_1}


def test_get_invalid_player_by_username(empty_players: Any, empty_games: Any) -> None:
    test_player_1: dict[str, str] = {
        "username": "Test1",
        "email": "test1@test.com",
        "first_name": "First1",
        "last_name": "Last1",
    }

    client.post("/player", json=test_player_1)

    response = client.get("/player/Test2")

    assert response.status_code == 404
