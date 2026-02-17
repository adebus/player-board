from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app

sqlite_url = "sqlite:///:memory:"

connect_args = {"check_same_thread": False}


def create_test_db_and_tables(db_engine: Engine) -> None:
    SQLModel.metadata.create_all(db_engine)


@pytest.fixture
def test_session() -> Generator[Session]:
    db_engine = create_engine(sqlite_url, connect_args=connect_args, poolclass=StaticPool)

    create_test_db_and_tables(db_engine)

    with Session(db_engine) as session:
        yield session

    db_engine.dispose()


@pytest.fixture
def test_client(test_session: Session) -> Generator[TestClient]:

    def get_session_override() -> Generator[Session]:
        yield test_session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()  # Cleanup
