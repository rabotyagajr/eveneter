from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import ScoreDetailCreate, ScoreDetailRead, ScoreDetailUpdate
from .controller import ScoreDetailController
from sqlalchemy.exc import SQLAlchemyError


score_details_router = APIRouter(prefix="/score_details", tags=["Score Details"])


@score_details_router.get("/", response_model=List[ScoreDetailRead])
async def get_score_details(db_session: DbSession):
    return await ScoreDetailController.get_all(db_session)


@score_details_router.get("/{id}", response_model=ScoreDetailRead)
async def get_score_detail(db_session: DbSession, id: int):
    result = await ScoreDetailController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Score detail not found"
        )
    return result


@score_details_router.post("/", response_model=ScoreDetailRead)
async def create_score_detail(
    db_session: DbSession,
    score_detail: ScoreDetailCreate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await ScoreDetailController.create(db_session, score_detail)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@score_details_router.patch("/{id}", response_model=ScoreDetailRead)
async def update_score_detail(
    db_session: DbSession,
    id: int,
    score_detail: ScoreDetailUpdate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await ScoreDetailController.update(db_session, id, score_detail)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@score_details_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_score_detail(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
):
    try:
        await ScoreDetailController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
