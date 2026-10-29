"""Composition root: tempat satu-satunya objek konkret dirakit."""
from functools import lru_cache

from fastapi import Depends

from app.repositories.base import ReservationRepository, RoomRepository
from app.repositories.in_memory import (
    InMemoryReservationRepository,
    InMemoryRoomRepository,
)
from app.services.reservation_service import ReservationService
from app.services.room_service import RoomService
from app.services.rules import default_rules


@lru_cache
def get_room_repo() -> RoomRepository:
    return InMemoryRoomRepository()


@lru_cache
def get_reservation_repo() -> ReservationRepository:
    return InMemoryReservationRepository()


def get_room_service(repo: RoomRepository = Depends(get_room_repo)) -> RoomService:
    return RoomService(repo)


def get_reservation_service(
    reservation_repo: ReservationRepository = Depends(get_reservation_repo),
    room_repo: RoomRepository = Depends(get_room_repo),
) -> ReservationService:
    return ReservationService(
        reservation_repo=reservation_repo,
        room_repo=room_repo,
        rules=default_rules(),
    )
