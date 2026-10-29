from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app import dependencies
from app.main import app
from app.repositories.in_memory import (
    InMemoryReservationRepository,
    InMemoryRoomRepository,
)
from app.services.reservation_service import ReservationService
from app.services.room_service import RoomService
from app.services.rules import default_rules


def dt(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, 1, hour, minute)


@pytest.fixture
def room_repo():
    return InMemoryRoomRepository()


@pytest.fixture
def reservation_repo():
    return InMemoryReservationRepository()


@pytest.fixture
def room_service(room_repo):
    return RoomService(room_repo)


@pytest.fixture
def reservation_service(reservation_repo, room_repo):
    return ReservationService(reservation_repo, room_repo, default_rules())


@pytest.fixture
def room(room_service):
    return room_service.create_room("Ruang A", 10)


@pytest.fixture
def client(room_repo, reservation_repo):
    """TestClient dengan repository baru tiap test (data terisolasi)."""
    app.dependency_overrides[dependencies.get_room_repo] = lambda: room_repo
    app.dependency_overrides[dependencies.get_reservation_repo] = (
        lambda: reservation_repo
    )
    yield TestClient(app)
    app.dependency_overrides.clear()
