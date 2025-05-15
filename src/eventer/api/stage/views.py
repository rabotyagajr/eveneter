from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import StageCreate, StageUpdate, StageRead
from .controller import StageController
from sqlalchemy.exc import SQLAlchemyError


stage_router = APIRouter(prefix="/stages", tags=["Stages"])


@stage_router.get("/{id}", response_model=StageRead)
async def get(db_session: DbSession, id: int) -> StageRead:
    result = await StageController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stage not found"
        )
    return result


@stage_router.get("/", response_model=List[StageRead])
async def get_all(db_session: DbSession) -> List[StageRead]:
    return await StageController.get_all(db_session)


@stage_router.post("/", response_model=StageRead)
async def create(
    db_session: DbSession, data: StageCreate, user: dict = Depends(get_current_user)
) -> StageRead:
    try:
        result = await StageController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_router.patch("/{id}", response_model=StageRead)
async def update(
    db_session: DbSession,
    id: int,
    data: StageUpdate,
    user: dict = Depends(get_current_user),
) -> StageRead:
    try:
        result = await StageController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stage_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await StageController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
