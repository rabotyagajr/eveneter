from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import User
from .schema import UserRead, UserCreate, UserUpdate


class UserController:

    @staticmethod
    async def get_one(db_session: AsyncSession, id: int) -> Optional[UserRead]:
        result = await db_session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[UserRead]:
        result = await db_session.execute(select(User))
        users = result.scalars().all()
        return users if users else []

    @staticmethod
    async def create(db_session: AsyncSession, data: UserCreate) -> UserRead:
        new_user = User(**data.model_dump())
        try:
            db_session.add(new_user)
            await db_session.commit()
            await db_session.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: UserUpdate) -> UserRead:
        user = await db_session.get(User, id)
        if not user:
            raise ValueError(f"User with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValueError("No fields provided for update")

        for key, value in update_data.items():
            setattr(user, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update user")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        user = await db_session.get(User, id)
        if not user:
            raise ValueError(f"User with ID {id} not found")
        try:
            await db_session.delete(user)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete user")
