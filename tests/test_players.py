from fastapi.testclient import TestClient


def test_post_players(test_client: TestClient) -> None:
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    response = test_client.post("/players", json=test_player)

    assert response.status_code == 201
    assert response.json() == {**test_player, "id": 1, "games": []}


def test_post_duplicate_player(test_client: TestClient) -> None:
    test_player: dict[str, str] = {
        "username": "Test",
        "email": "test@test.com",
        "first_name": "First",
        "last_name": "Last",
    }

    test_client.post("/players", json=test_player)
    response = test_client.post("/players", json=test_player)

    assert response.status_code == 409


def test_get_all_players(test_client: TestClient) -> None:
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

    response_player_1: dict[str, str | int | list[str | None]] = {
        "username": test_player_1["username"],
        "email": test_player_1["email"],
        "first_name": test_player_1["first_name"],
        "last_name": test_player_1["last_name"],
        "id": 1,
        "games": [],
    }

    response_player_2: dict[str, str | int | list[str | None]] = {
        "username": test_player_2["username"],
        "email": test_player_2["email"],
        "first_name": test_player_2["first_name"],
        "last_name": test_player_2["last_name"],
        "id": 2,
        "games": [],
    }

    test_client.post("/players", json=test_player_1)
    test_client.post("/players", json=test_player_2)

    response = test_client.get("/players")

    assert response.status_code == 200
    assert response.json() == [response_player_1, response_player_2]


def test_get_all_players_no_players(test_client: TestClient) -> None:
    response = test_client.get("/players")

    assert response.status_code == 200
    assert response.json() == []


def test_get_player_by_username(test_client: TestClient) -> None:
    test_player_1: dict[str, str] = {
        "username": "Test1",
        "email": "test1@test.com",
        "first_name": "First1",
        "last_name": "Last1",
    }

    response_player_1: dict[str, str | int | list[str | None]] = {
        "username": test_player_1["username"],
        "email": test_player_1["email"],
        "first_name": test_player_1["first_name"],
        "last_name": test_player_1["last_name"],
        "id": 1,
        "games": [],
    }

    test_client.post("/players", json=test_player_1)

    response = test_client.get("/players/Test1")

    assert response.status_code == 200
    assert response.json() == response_player_1


def test_get_invalid_player_by_username(test_client: TestClient) -> None:
    test_player_1: dict[str, str] = {
        "username": "Test1",
        "email": "test1@test.com",
        "first_name": "First1",
        "last_name": "Last1",
    }

    test_client.post("/players", json=test_player_1)

    response = test_client.get("/players/Test2")

    assert response.status_code == 404
