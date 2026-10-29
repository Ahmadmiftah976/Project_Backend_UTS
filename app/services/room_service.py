from app.exceptions import NotFoundError
from app.models.room import Room
from app.repositories.base import RoomRepository


class RoomService:
    def __init__(self, repo: RoomRepository) -> None:
        self._repo = repo

    def create_room(self, name: str, capacity: int) -> Room:
        return self._repo.add(name=name, capacity=capacity)

    def get_room(self, room_id: int) -> Room:
        room = self._repo.get(room_id)
        if room is None:
            raise NotFoundError(f"Ruangan dengan id {room_id} tidak ditemukan.")
        return room

    def list_rooms(self) -> list[Room]:
        return self._repo.list_all()
