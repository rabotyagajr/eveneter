from typing import List
from eventer.auth.auth import get_current_user
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.database.database import DbSession
from .schema import ParameterCreate, ParameterUpdate, ParameterRead
from .controller import ParameterController
from sqlalchemy.exc import SQLAlchemyError


parameter_router = APIRouter(prefix="/parameters", tags=["Parameters"])


@parameter_router.get("/", response_model=List[ParameterRead])
async def get_all(db_session: DbSession) -> List[ParameterRead]:
    return await ParameterController.get_all(db_session)


@parameter_router.get("/{id}", response_model=ParameterRead)
async def get(db_session: DbSession, id: int) -> ParameterRead:
    result = await ParameterController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found"
        )
    return result


@parameter_router.post("/", response_model=ParameterRead)
async def create(
    db_session: DbSession, data: ParameterCreate, user: dict = Depends(get_current_user)
) -> ParameterRead:
    try:
        result = await ParameterController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@parameter_router.patch("/{id}", response_model=ParameterRead)
async def update(
    db_session: DbSession,
    id: int,
    data: ParameterUpdate,
    user: dict = Depends(get_current_user),
) -> ParameterRead:
    try:
        result = await ParameterController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@parameter_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await ParameterController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
