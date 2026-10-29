"""Abstraksi repository (Dependency Inversion Principle).

Service hanya bergantung pada interface ini, bukan pada implementasi konkret.
Jika nanti ingin pindah ke SQLite/PostgreSQL, cukup buat implementasi baru
tanpa mengubah service sama sekali.
"""
from abc import ABC, abstractmethod
from typing import Optional

from app.models.reservation import Reservation
from app.models.room import Room


class RoomRepository(ABC):
    @abstractmethod
    def add(self, name: str, capacity: int) -> Room: ...

    @abstractmethod
    def get(self, room_id: int) -> Optional[Room]: ...

    @abstractmethod
    def list_all(self) -> list[Room]: ...


class ReservationRepository(ABC):
    @abstractmethod
    def add(self, reservation: Reservation) -> Reservation: ...

    @abstractmethod
    def get(self, reservation_id: int) -> Optional[Reservation]: ...

    @abstractmethod
    def list_all(self) -> list[Reservation]: ...

    @abstractmethod
    def list_by_room(self, room_id: int) -> list[Reservation]: ...

    @abstractmethod
    def update(self, reservation: Reservation) -> Reservation: ...
