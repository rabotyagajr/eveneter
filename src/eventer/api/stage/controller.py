from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import Stage
from .schema import StageCreate, StageRead, StageUpdate


class StageController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[StageRead]:
        result = await db_session.execute(select(Stage).where(Stage.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[StageRead]:
        result = await db_session.execute(select(Stage))
        stages = result.scalars().all()
        return stages if stages else []

    @staticmethod
    async def create(db_session: AsyncSession, stage: StageCreate) -> StageRead:
        try:
            stage = Stage(**stage.model_dump())
            db_session.add(stage)
            await db_session.commit()
            await db_session.refresh(stage)
            return stage
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to create stage")

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, stage: StageUpdate
    ) -> StageRead:
        try:
            stage = await db_session.get(Stage, id)
            if not stage:
                raise ValueError(f"Stage with ID {id} not found")
            update_data = stage.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("No fields provided for update")
            for key, value in update_data.items():
                setattr(stage, key, value)
            await db_session.commit()
            await db_session.refresh(stage)
            return stage
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to update stage")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        stage = await db_session.get(Stage, id)
        if not stage:
            raise ValueError(f"Stage with ID {id} not found")
        try:
            await db_session.delete(stage)
            await db_session.commit()
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to delete stage")
