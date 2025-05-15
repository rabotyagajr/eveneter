from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from eventer.database.database import DbSession
from eventer.api.stage_team_transitions.schema import (
    StageTeamTransitionCreate,
    StageTeamTransitionRead,
    StageTeamTransitionUpdate,
)
from .controller import TeamController

stage_team_transitions_router = APIRouter(
    prefix="/stage_team_transition", tags=["Stage team transition"]
)


@stage_team_transitions_router.get(
    "/",
    response_model=list[StageTeamTransitionRead],
    summary="Получить все переходы команд",
)
async def get_all_stage_team_transitions(
    db_session: DbSession,
) -> list[StageTeamTransitionRead]:
    stage_team_transitions = await TeamController.get_all(db_session)
    return stage_team_transitions


@stage_team_transitions_router.get("/{id}", response_model=StageTeamTransitionRead)
async def get_stage_team_transitions(
    db_session: DbSession, id: int
) -> StageTeamTransitionRead:
    stage_team_transitions = await TeamController.get(db_session, id)

    if not stage_team_transitions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transitions not found"
        )

    return stage_team_transitions


@stage_team_transitions_router.patch("/{id}", response_model=StageTeamTransitionUpdate)
async def update_stage_team_transitions(
    db_session: DbSession,
    id: int,
    data: StageTeamTransitionUpdate,
    user: dict = Depends(get_current_user),
) -> StageTeamTransitionUpdate:
    try:
        stage_team_transitions = await TeamController.update(db_session, id, data)
        return stage_team_transitions
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_team_transitions_router.post("/", response_model=StageTeamTransitionCreate)
async def create_stage_team_transitions(
    db_session: DbSession,
    data: StageTeamTransitionCreate,
    user: dict = Depends(get_current_user),
) -> StageTeamTransitionCreate:
    try:
        stage_team_transition = await TeamController.create(db_session, data)
        return stage_team_transition
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_team_transitions_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
