from typing import List
from sqlalchemy.exc import SQLAlchemyError
from eventer.api.city.schema import CityCreate, CityUpdate, CityRead
from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.database.database import DbSession
from .controller import CityController
from eventer.auth.auth import get_current_user

city_router = APIRouter(prefix="/cities", tags=["Cities"])


@city_router.get("/", response_model=List[CityRead])
async def get_cities(db_session: DbSession):
    cities = await CityController.get_all(db_session=db_session)
    return cities


@city_router.get("/{id}", response_model=CityRead)
async def get_city_by_id(id: int, db_session: DbSession):
    city = await CityController.get_one(
        db_session=db_session,
        id=id,
    )

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return city


@city_router.patch(
    "/{id}",
    response_model=CityRead,
    status_code=status.HTTP_200_OK,
)
async def patch_city(
    db_session: DbSession,
    id: int,
    data: CityUpdate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await CityController.patch_city(
            db_session=db_session, id=id, data=data
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )


@city_router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_city(
    db_session: DbSession, data: CityCreate, user: dict = Depends(get_current_user)
):
    try:
        city = await CityController.create_city(db_session=db_session, data=data)
        return city
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )


@city_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
):
    city = await CityController.get_one(db_session, id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    try:
        await CityController.delete_city(
            db_session=db_session,
            city=city,
        )
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content=f"City with id {id} deleted",
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete city",
        )
