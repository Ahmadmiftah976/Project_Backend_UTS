import pytest

from app.exceptions import NotFoundError


def test_create_room(room_service):
    room = room_service.create_room("Ruang B", 5)
    assert room.id == 1
    assert room.name == "Ruang B"
    assert room.capacity == 5


def test_list_rooms(room_service):
    room_service.create_room("A", 1)
    room_service.create_room("B", 2)
    assert len(room_service.list_rooms()) == 2


def test_get_room_not_found(room_service):
    with pytest.raises(NotFoundError):
        room_service.get_room(999)
