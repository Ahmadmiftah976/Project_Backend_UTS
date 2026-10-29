from fastapi import APIRouter, Depends, status

from app.dependencies import get_room_service
from app.schemas.room import RoomCreate, RoomResponse
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(payload: RoomCreate, service: RoomService = Depends(get_room_service)):
    return service.create_room(payload.name, payload.capacity)


@router.get("", response_model=list[RoomResponse])
def list_rooms(service: RoomService = Depends(get_room_service)):
    return service.list_rooms()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, service: RoomService = Depends(get_room_service)):
    return service.get_room(room_id)
