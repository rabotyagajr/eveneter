from fastapi import APIRouter, HTTPException, status, Response, Depends
from typing import List
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import LeaderBoardCreate, LeaderBoardUpdate, LeaderBoardRead
from .controller import LeaderBoardController
from sqlalchemy.exc import SQLAlchemyError

leaderboard_router = APIRouter(prefix="/leaderboards", tags=["Leaderboards"])


@leaderboard_router.get("/", response_model=List[LeaderBoardRead])
async def get_all(db_session: DbSession) -> List[LeaderBoardRead]:
    return await LeaderBoardController.get_all(db_session)


@leaderboard_router.get("/{id}", response_model=LeaderBoardRead)
async def get(db_session: DbSession, id: int) -> LeaderBoardRead:
    result = await LeaderBoardController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Leaderboard not found"
        )
    return result


@leaderboard_router.post("/", response_model=LeaderBoardRead)
async def create(
    db_session: DbSession,
    data: LeaderBoardCreate,
    user: dict = Depends(get_current_user),
) -> LeaderBoardRead:
    try:
        result = await LeaderBoardController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@leaderboard_router.patch("/{id}", response_model=LeaderBoardRead)
async def update(
    db_session: DbSession,
    id: int,
    data: LeaderBoardUpdate,
    user: dict = Depends(get_current_user),
) -> LeaderBoardRead:
    try:
        result = await LeaderBoardController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@leaderboard_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await LeaderBoardController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
