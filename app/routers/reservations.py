from typing import Optional

from fastapi import APIRouter, Depends, status

from app.dependencies import get_reservation_service
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post(
    "", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
def create_reservation(
    payload: ReservationCreate,
    service: ReservationService = Depends(get_reservation_service),
):
    return service.create_reservation(
        payload.room_id, payload.booked_by, payload.start_time, payload.end_time
    )


@router.get("", response_model=list[ReservationResponse])
def list_reservations(
    room_id: Optional[int] = None,
    service: ReservationService = Depends(get_reservation_service),
):
    return service.list_reservations(room_id)


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_reservation_service),
):
    return service.get_reservation(reservation_id)


@router.patch("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancel_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_reservation_service),
):
    return service.cancel_reservation(reservation_id)
