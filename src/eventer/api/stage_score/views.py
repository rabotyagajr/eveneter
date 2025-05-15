from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.database.database import DbSession
from .schema import StageScoreCreate, StageScoreUpdate, StageScoreRead
from .controller import StageScoreController
from sqlalchemy.exc import SQLAlchemyError
from eventer.auth.auth import get_current_user

stage_score_router = APIRouter(prefix="/stage_scores", tags=["Stage Scores"])


@stage_score_router.get("/", response_model=List[StageScoreRead])
async def get_all(db_session: DbSession) -> List[StageScoreRead]:
    return await StageScoreController.get_all(db_session)


@stage_score_router.get("/{id}", response_model=StageScoreRead)
async def get(db_session: DbSession, id: int) -> Optional[StageScoreRead]:
    return await StageScoreController.get(db_session, id)


@stage_score_router.post("/", response_model=StageScoreRead)
async def create(
    db_session: DbSession, stage_score: StageScoreCreate, user: dict = Depends(get_current_user)
) -> StageScoreRead:
    try:
        result = await StageScoreController.create(db_session, stage_score)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_score_router.patch("/{id}", response_model=StageScoreRead)
async def update(
    db_session: DbSession,
    id: int,
    stage_score: StageScoreUpdate,
    user: dict = Depends(get_current_user),
) -> StageScoreRead:
    try:
        result = await StageScoreController.update(db_session, id, stage_score)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_score_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db_session: DbSession, id: int, user: dict = Depends(get_current_user)) -> None:
    try:
        await StageScoreController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
