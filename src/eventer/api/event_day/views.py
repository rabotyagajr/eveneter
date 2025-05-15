from fastapi import APIRouter, HTTPException, status, Response, Depends
from typing import List
from eventer.auth.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from eventer.database.database import DbSession
from eventer.api.event_day.schema import EventDayCreate, EventDayUpdate, EventDayRead
from .controller import EventDayController

eventdays_router = APIRouter(prefix="/event_days", tags=["Event Days"])


@eventdays_router.get("/{id}", response_model=EventDayRead)
async def get_event_day(id: int, db_session: DbSession):
    event_day = await EventDayController.get_one(db_session, id)
    if not event_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EventDay not found"
        )
    return event_day


@eventdays_router.get("/", response_model=List[EventDayRead])
async def get_event_days(db_session: DbSession):
    return await EventDayController.get_all(db_session)


@eventdays_router.post(
    "/", response_model=EventDayRead, status_code=status.HTTP_201_CREATED
)
async def create_event_day(
    db_session: DbSession, data: EventDayCreate, user: dict = Depends(get_current_user)
):
    return await EventDayController.create(db_session, data)


@eventdays_router.patch("/{id}", response_model=EventDayRead)
async def update_event_day(
    id: int,
    data: EventDayUpdate,
    db_session: DbSession,
    user: dict = Depends(get_current_user),
):
    try:
        return await EventDayController.update(db_session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@eventdays_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_day(
    id: int,
    db_session: DbSession,
    user: dict = Depends(get_current_user)
):
    try:
        await EventDayController.delete(db_session, id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content=f"City with id {id} deleted",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
