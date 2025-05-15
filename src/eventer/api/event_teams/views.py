from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import EventTeamCreate, EventTeamRead, EventTeamUpdate
from .controller import EventTeamController
from sqlalchemy.exc import SQLAlchemyError


event_teams_router = APIRouter(prefix="/event_teams", tags=["Event Teams"])


@event_teams_router.get("/", response_model=List[EventTeamRead])
async def get_all_event_teams(db_session: DbSession) -> List[EventTeamRead]:
    return await EventTeamController.get_all(db_session)


@event_teams_router.get("/{id}", response_model=EventTeamRead)
async def get_event_team(db_session: DbSession, id: int = None) -> EventTeamRead:
    result = await EventTeamController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event team not found"
        )
    return result


@event_teams_router.post("/", response_model=EventTeamRead)
async def create_event_team(
    db_session: DbSession,
    data: EventTeamCreate = None,
    user: dict = Depends(get_current_user),
) -> EventTeamRead:
    try:
        result = await EventTeamController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_teams_router.patch("/{id}", response_model=EventTeamRead)
async def update_event_team(
    db_session: DbSession,
    id: int = None,
    data: EventTeamUpdate = None,
    user: dict = Depends(get_current_user),
) -> EventTeamRead:
    try:
        result = await EventTeamController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_teams_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_team(
    db_session: DbSession, id: int = None, user: dict = Depends(get_current_user)
) -> None:
    try:
        await EventTeamController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
