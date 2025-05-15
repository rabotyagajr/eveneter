from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from eventer.api.team_members.schema import (
    TeamMemberCreate,
    TeamMemberUpdate,
    TeamMemberRead,
)
from .controller import TeamMemberController
from sqlalchemy.exc import SQLAlchemyError

team_members_router = APIRouter(prefix="/team_members", tags=["Team Members"])


@team_members_router.get("/", response_model=list[TeamMemberRead])
async def get_all_teams_members(db_session: DbSession) -> list[TeamMemberRead]:
    team_members = await TeamMemberController.get_all(db_session)
    return team_members


@team_members_router.post("/", response_model=TeamMemberRead)
async def create_team_member(
    db_session: DbSession,
    data: TeamMemberCreate,
    user: dict = Depends(get_current_user),
) -> TeamMemberRead:
    try:
        team_member = await TeamMemberController.create(db_session, data)
        return team_member
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@team_members_router.get("/team/{team_id}", response_model=list[TeamMemberRead])
async def get_all_team_members(
    db_session: DbSession, team_id: int
) -> list[TeamMemberRead]:
    team_members = await TeamMemberController.get_all_by_team(db_session, team_id)
    return team_members


@team_members_router.get("/user/{user_id}", response_model=list[TeamMemberRead])
async def get_all_user_teams(
    db_session: DbSession, user_id: int
) -> list[TeamMemberRead]:
    teams_member = await TeamMemberController.get_all_by_user(db_session, user_id)
    return teams_member


@team_members_router.get("/{team_id}/{user_id}", response_model=TeamMemberRead)
async def get_team_member(
    db_session: DbSession, user_id: int, team_id: int
) -> TeamMemberRead:
    team_member = await TeamMemberController.get_one(
        db_session, user_id=user_id, team_id=team_id
    )

    if not team_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found"
        )

    return team_member


@team_members_router.patch("/{team_id}/{user_id}", response_model=TeamMemberRead)
async def update_team_member(
    db_session: DbSession,
    user_id: int,
    team_id: int,
    data: TeamMemberUpdate,
    user: dict = Depends(get_current_user),
) -> TeamMemberRead:
    try:
        team_member = await TeamMemberController.update(
            db_session, user_id=user_id, team_id=team_id, data=data
        )
        return team_member
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@team_members_router.delete(
    "/{team_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_team_member(
    db_session: DbSession,
    user_id: int,
    team_id: int,
    user: dict = Depends(get_current_user),
) -> None:
    try:
        await TeamMemberController.delete(db_session, user_id=user_id, team_id=team_id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, detail="Team member deleted"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
