from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReservationCreate(BaseModel):
    room_id: int
    booked_by: str = Field(min_length=1, max_length=100)
    start_time: datetime
    end_time: datetime


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    booked_by: str
    start_time: datetime
    end_time: datetime
    status: str
