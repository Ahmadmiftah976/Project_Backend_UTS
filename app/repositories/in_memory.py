"""Implementasi repository yang menyimpan data di memori (dict)."""
from dataclasses import replace
from typing import Optional

from app.models.reservation import Reservation
from app.models.room import Room
from app.repositories.base import ReservationRepository, RoomRepository


class InMemoryRoomRepository(RoomRepository):
    def __init__(self) -> None:
        self._data: dict[int, Room] = {}
        self._next_id = 1

    def add(self, name: str, capacity: int) -> Room:
        room = Room(id=self._next_id, name=name, capacity=capacity)
        self._data[room.id] = room
        self._next_id += 1
        return room

    def get(self, room_id: int) -> Optional[Room]:
        return self._data.get(room_id)

    def list_all(self) -> list[Room]:
        return list(self._data.values())


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self) -> None:
        self._data: dict[int, Reservation] = {}
        self._next_id = 1

    def add(self, reservation: Reservation) -> Reservation:
        saved = replace(reservation, id=self._next_id)
        self._data[saved.id] = saved
        self._next_id += 1
        return saved

    def get(self, reservation_id: int) -> Optional[Reservation]:
        return self._data.get(reservation_id)

    def list_all(self) -> list[Reservation]:
        return list(self._data.values())

    def list_by_room(self, room_id: int) -> list[Reservation]:
        return [r for r in self._data.values() if r.room_id == room_id]

    def update(self, reservation: Reservation) -> Reservation:
        self._data[reservation.id] = reservation
        return reservation
