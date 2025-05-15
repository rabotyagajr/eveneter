from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from eventer.database.database import DbSession
from eventer.api.team.schema import TeamCreate, TeamUpdate, TeamRead
from .controller import TeamController

team_router = APIRouter(prefix="/teams", tags=["Teams"])


@team_router.get("/", response_model=list[TeamRead])
async def get_all_teams(db_session: DbSession) -> list[TeamRead]:
    teams = await TeamController.get_all(db_session)
    return teams


@team_router.get("/{id}", response_model=TeamRead)
async def get_team(db_session: DbSession, id: int) -> TeamRead:
    team = await TeamController.get(db_session, id)

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    return team


@team_router.patch("/{id}", response_model=TeamUpdate)
async def update_team(
    db_session: DbSession,
    id: int,
    data: TeamUpdate,
    user: dict = Depends(get_current_user),
) -> TeamUpdate:
    try:
        team = await TeamController.update(db_session, id, data)
        return team
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@team_router.post("/", response_model=TeamCreate)
async def create_team(
    db_session: DbSession, data: TeamCreate, user: dict = Depends(get_current_user)
) -> TeamCreate:
    try:
        team = await TeamController.create(db_session, data)
        return team
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@team_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await TeamController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
