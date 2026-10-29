import pytest

from app.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.services.reservation_service import ReservationService
from tests.conftest import dt


def test_create_reservation_success(reservation_service, room):
    r = reservation_service.create_reservation(room.id, "Budi", dt(9), dt(11))
    assert r.id == 1
    assert r.status == "active"


def test_create_reservation_room_not_found(reservation_service):
    with pytest.raises(NotFoundError):
        reservation_service.create_reservation(99, "Budi", dt(9), dt(10))


def test_create_reservation_overlap_raises_conflict(reservation_service, room):
    reservation_service.create_reservation(room.id, "Budi", dt(9), dt(11))
    with pytest.raises(ConflictError):
        reservation_service.create_reservation(room.id, "Ani", dt(10), dt(12))


def test_create_reservation_too_long(reservation_service, room):
    with pytest.raises(BusinessRuleError):
        reservation_service.create_reservation(room.id, "Budi", dt(8), dt(12))


def test_same_time_different_room_is_allowed(reservation_service, room_service, room):
    other = room_service.create_room("Ruang B", 4)
    reservation_service.create_reservation(room.id, "Budi", dt(9), dt(11))
    r = reservation_service.create_reservation(other.id, "Ani", dt(9), dt(11))
    assert r.room_id == other.id


def test_cancel_then_slot_can_be_rebooked(reservation_service, room):
    r = reservation_service.create_reservation(room.id, "Budi", dt(9), dt(11))
    cancelled = reservation_service.cancel_reservation(r.id)
    assert cancelled.status == "cancelled"
    again = reservation_service.create_reservation(room.id, "Ani", dt(9), dt(11))
    assert again.status == "active"


def test_cancel_not_found(reservation_service):
    with pytest.raises(NotFoundError):
        reservation_service.cancel_reservation(404)


def test_list_reservations_filter_by_room(reservation_service, room_service, room):
    other = room_service.create_room("B", 3)
    reservation_service.create_reservation(room.id, "Budi", dt(9), dt(10))
    reservation_service.create_reservation(other.id, "Ani", dt(9), dt(10))
    assert len(reservation_service.list_reservations()) == 2
    assert len(reservation_service.list_reservations(room.id)) == 1


def test_service_uses_injected_rules_only(reservation_repo, room_repo, room):
    """Bukti OCP/DIP: tanpa rules, service tidak menolak apa pun."""
    service = ReservationService(reservation_repo, room_repo, rules=[])
    service.create_reservation(room.id, "Budi", dt(9), dt(10))
    service.create_reservation(room.id, "Ani", dt(9), dt(10))
    assert len(service.list_reservations()) == 2
