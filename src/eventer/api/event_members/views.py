from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import EventMemberCreate, EventMemberRead, EventMemberUpdate
from .controller import EventMemberController
from sqlalchemy.exc import SQLAlchemyError


event_members_router = APIRouter(prefix="/event_members", tags=["Event Members"])


@event_members_router.get("/", response_model=List[EventMemberRead])
async def get_all(db_session: DbSession):
    return await EventMemberController.get_all(db_session)


@event_members_router.get("/{id}", response_model=EventMemberRead)
async def get(db_session: DbSession, id: int = None):
    result = await EventMemberController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event member not found"
        )
    return result


@event_members_router.post("/", response_model=EventMemberRead)
async def create(
    db_session: DbSession,
    data: EventMemberCreate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await EventMemberController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_members_router.patch("/{id}", response_model=EventMemberRead)
async def update(
    db_session: DbSession,
    id: int,
    data: EventMemberUpdate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await EventMemberController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_members_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
):
    try:
        await EventMemberController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
