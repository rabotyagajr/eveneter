from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from eventer.api.user.schema import UserCreate, UserUpdate, UserRead
from .controller import UserController
from sqlalchemy.exc import SQLAlchemyError

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/{id}", response_model=UserRead)
async def get_user(db_session: DbSession, id: int) -> UserRead:
    result = await UserController.get_one(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return result


@user_router.get("/", response_model=list[UserRead])
async def get_all_users(db_session: DbSession) -> list[UserRead]:
    return await UserController.get_all(db_session)


@user_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    db_session: DbSession, data: UserCreate, user: dict = Depends(get_current_user)
) -> UserRead:
    return await UserController.create(db_session, data)


@user_router.patch("/{id}", response_model=UserCreate, status_code=status.HTTP_200_OK)
async def update_user(
    db_session: DbSession,
    id: int,
    data: UserUpdate,
    user: dict = Depends(get_current_user),
) -> UserRead:
    try:
        return await UserController.update(db_session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# !TODO fix foreign key exception
@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await UserController.delete(db_session, id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content=f"User with id {id} deleted",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
