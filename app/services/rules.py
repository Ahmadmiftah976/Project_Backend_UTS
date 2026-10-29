"""Aturan validasi reservasi.

Setiap aturan = satu class dengan satu tanggung jawab (SRP).
Menambah aturan baru cukup membuat class baru turunan ReservationRule
lalu mendaftarkannya, TANPA mengubah ReservationService (Open/Closed Principle).
Semua aturan bisa saling menggantikan lewat interface yang sama (Liskov).
"""
from abc import ABC, abstractmethod
from datetime import timedelta

from app.exceptions import BusinessRuleError, ConflictError
from app.models.reservation import Reservation


class ReservationRule(ABC):
    @abstractmethod
    def validate(self, new: Reservation, existing: list[Reservation]) -> None:
        """Raise DomainError jika reservasi `new` melanggar aturan."""


class TimeOrderRule(ReservationRule):
    def validate(self, new: Reservation, existing: list[Reservation]) -> None:
        if new.end_time <= new.start_time:
            raise BusinessRuleError("Waktu selesai harus setelah waktu mulai.")


class MaxDurationRule(ReservationRule):
    def __init__(self, max_hours: int = 3) -> None:
        self._max = timedelta(hours=max_hours)
        self._max_hours = max_hours

    def validate(self, new: Reservation, existing: list[Reservation]) -> None:
        if new.end_time - new.start_time > self._max:
            raise BusinessRuleError(
                f"Durasi reservasi maksimal {self._max_hours} jam."
            )


class NoOverlapRule(ReservationRule):
    def validate(self, new: Reservation, existing: list[Reservation]) -> None:
        for other in existing:
            if other.is_active and new.overlaps_with(other):
                raise ConflictError(
                    "Jadwal bentrok dengan reservasi lain pada ruangan ini."
                )


def default_rules() -> list[ReservationRule]:
    return [TimeOrderRule(), MaxDurationRule(max_hours=3), NoOverlapRule()]
