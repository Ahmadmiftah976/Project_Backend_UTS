from datetime import datetime

from app.exceptions import NotFoundError
from app.models.reservation import Reservation
from app.repositories.base import ReservationRepository, RoomRepository
from app.services.rules import ReservationRule


class ReservationService:
    """Mengorkestrasi pembuatan/pembatalan reservasi.

    Semua dependency di-inject lewat constructor (Dependency Inversion),
    sehingga mudah diganti/di-mock saat unit test.
    """

    def __init__(
        self,
        reservation_repo: ReservationRepository,
        room_repo: RoomRepository,
        rules: list[ReservationRule],
    ) -> None:
        self._reservations = reservation_repo
        self._rooms = room_repo
        self._rules = rules

    def create_reservation(
        self, room_id: int, booked_by: str, start_time: datetime, end_time: datetime
    ) -> Reservation:
        if self._rooms.get(room_id) is None:
            raise NotFoundError(f"Ruangan dengan id {room_id} tidak ditemukan.")

        candidate = Reservation(
            id=0,
            room_id=room_id,
            booked_by=booked_by,
            start_time=start_time,
            end_time=end_time,
        )
        existing = self._reservations.list_by_room(room_id)
        for rule in self._rules:
            rule.validate(candidate, existing)

        return self._reservations.add(candidate)

    def get_reservation(self, reservation_id: int) -> Reservation:
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            raise NotFoundError(
                f"Reservasi dengan id {reservation_id} tidak ditemukan."
            )
        return reservation

    def list_reservations(self, room_id: int | None = None) -> list[Reservation]:
        if room_id is None:
            return self._reservations.list_all()
        return self._reservations.list_by_room(room_id)

    def cancel_reservation(self, reservation_id: int) -> Reservation:
        reservation = self.get_reservation(reservation_id)
        reservation.status = "cancelled"
        return self._reservations.update(reservation)
