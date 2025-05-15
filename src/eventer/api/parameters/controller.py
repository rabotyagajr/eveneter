from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import Parameter
from .schema import ParameterCreate, ParameterRead, ParameterUpdate


class ParameterController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[ParameterRead]:
        result = await db_session.execute(select(Parameter).where(Parameter.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[ParameterRead]:
        result = await db_session.execute(select(Parameter))
        parameters = result.scalars().all()
        return parameters if parameters else []

    @staticmethod
    async def create(db_session: AsyncSession, data: ParameterCreate) -> ParameterRead:
        new_parameter = Parameter(**data.model_dump())
        try:
            db_session.add(new_parameter)
            await db_session.commit()
            await db_session.refresh(new_parameter)
            return new_parameter
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to create parameter")

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, data: ParameterUpdate
    ) -> ParameterRead:
        parameter = await db_session.get(Parameter, id)
        if not parameter:
            raise ValueError(f"Parameter with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(parameter, key, value)
        if update_data:
            raise ValueError("No fields provided for update")
        try:
            await db_session.commit()
            await db_session.refresh(parameter)
            return parameter
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update parameter")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        parameter = await db_session.get(Parameter, id)
        if not parameter:
            raise ValueError(f"Parameter with ID {id} not found")
        try:
            await db_session.delete(parameter)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete parameter")
