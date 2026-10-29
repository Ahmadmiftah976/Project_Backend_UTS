from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reservation:
    id: int
    room_id: int
    booked_by: str
    start_time: datetime
    end_time: datetime
    status: str = "active"  # "active" | "cancelled"

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    def overlaps_with(self, other: "Reservation") -> bool:
        """Dua jadwal bentrok jika rentangnya saling tumpang tindih.
        Jadwal yang 'menempel' (selesai 10:00, mulai 10:00) tidak dianggap bentrok."""
        return self.start_time < other.end_time and other.start_time < self.end_time
