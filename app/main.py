from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.routers import reservations, rooms

app = FastAPI(
    title="Room Reservation API",
    description="Sistem reservasi ruang belajar / ruang rapat (in-memory).",
    version="1.0.0",
)

app.include_router(rooms.router)
app.include_router(reservations.router)


def _error(status_code: int):
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return handler


app.add_exception_handler(NotFoundError, _error(404))
app.add_exception_handler(ConflictError, _error(409))
app.add_exception_handler(BusinessRuleError, _error(422))


@app.get("/", tags=["Health"])
def root():
    return {"message": "Room Reservation API is running"}
