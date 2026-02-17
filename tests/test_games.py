from fastapi.testclient import TestClient


def test_post_game(test_client: TestClient) -> None:
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

    result_game: dict[str, str | int | list[str | int]] = {
        "name": test_game["name"],
        "min_players": test_game["min_players"],
        "max_players": test_game["max_players"],
        "id": 1,
        "owners": [test_game["owner"]],
    }

    test_client.post("/players", json=test_player)
    response = test_client.post("/games", json=test_game)

    assert response.status_code == 201
    assert response.json() == result_game


def test_post_game_no_player(test_client: TestClient) -> None:

    test_game: dict[str, str | int] = {
        "name": "Everdell",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test",
    }

    response = test_client.post("/games", json=test_game)

    assert response.status_code == 404


def test_post_game_no_player_2(test_client: TestClient) -> None:
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

    test_client.post("/players", json=test_player)

    response = test_client.post("/games", json=test_game)

    assert response.status_code == 404


def test_post_duplicate_game(test_client: TestClient) -> None:
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

    test_client.post("/players", json=test_player)
    test_client.post("/games", json=test_game)
    response = test_client.post("/games", json=test_game)

    assert response.status_code == 409


def test_post_invalid_players(test_client: TestClient) -> None:
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

    test_client.post("/players", json=test_player)

    response = test_client.post("/games", json=test_game)

    assert response.status_code == 422


def test_get_game_1(test_client: TestClient) -> None:
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

    result_game: dict[str, str | int | list[str | int]] = {
        "name": test_game["name"],
        "min_players": test_game["min_players"],
        "max_players": test_game["max_players"],
        "id": 1,
        "owners": [test_game["owner"]],
    }

    test_client.post("/players", json=test_player)
    test_client.post("/games", json=test_game)

    response = test_client.get("/games")

    assert response.status_code == 200
    assert response.json() == [result_game]


def test_get_game_2(test_client: TestClient) -> None:
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

    result_game_1: dict[str, str | int | list[str | int]] = {
        "name": test_game_1["name"],
        "min_players": test_game_1["min_players"],
        "max_players": test_game_1["max_players"],
        "id": 1,
        "owners": [test_game_1["owner"]],
    }

    result_game_2: dict[str, str | int | list[str | int]] = {
        "name": test_game_2["name"],
        "min_players": test_game_2["min_players"],
        "max_players": test_game_2["max_players"],
        "id": 2,
        "owners": [test_game_2["owner"]],
    }

    test_client.post("/players", json=test_player)
    test_client.post("/games", json=test_game_1)
    test_client.post("/games", json=test_game_2)

    response = test_client.get("/games")

    assert response.status_code == 200
    assert response.json() == [result_game_1, result_game_2]


def test_read_all_games_no_games(test_client: TestClient) -> None:
    response = test_client.get("/games")

    assert response.status_code == 200
    assert response.json() == []


def test_get_specific_game(test_client: TestClient) -> None:
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

    result_game_2: dict[str, str | int | list[str | int]] = {
        "name": test_game_2["name"],
        "min_players": test_game_2["min_players"],
        "max_players": test_game_2["max_players"],
        "id": 2,
        "owners": [test_game_2["owner"]],
    }

    test_client.post("/players", json=test_player)
    test_client.post("/games", json=test_game_1)
    test_client.post("/games", json=test_game_2)

    response = test_client.get(f"/games/{test_player['username']}/{test_game_2['name']}")

    assert response.status_code == 200
    assert response.json() == result_game_2


def test_get_game_by_owner_no_game(test_client: TestClient) -> None:
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

    test_client.post("/players", json=test_player)
    test_client.post("/games", json=test_game_2)

    response = test_client.get(f"/games/{test_player['username']}/Clank")

    assert response.status_code == 404


def test_get_game_by_owner_not_owned_by_owner(test_client: TestClient) -> None:
    test_game_2: dict[str, str | int] = {
        "name": "Gloomhaven",
        "min_players": 1,
        "max_players": 4,
        "owner": "Test1",
    }
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

    test_client.post("/players", json=test_player_1)
    test_client.post("/players", json=test_player_2)
    test_client.post("/games", json=test_game_2)

    response = test_client.get(f"/games/{test_player_2['username']}/{test_game_2['name']}")

    assert response.status_code == 404


def test_get_specific_game_failure(test_client: TestClient) -> None:
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

    test_client.post("/players", json=test_player)

    test_client.post("/games", json=test_game_1)
    test_client.post("/games", json=test_game_2)

    response = test_client.get("/games/Test2/Clank")

    assert response.status_code == 404
