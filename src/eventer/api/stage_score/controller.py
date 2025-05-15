from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import StageScore
from .schema import StageScoreCreate, StageScoreRead, StageScoreUpdate


class StageScoreController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[StageScoreRead]:
        result = await db_session.execute(select(StageScore).where(StageScore.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[StageScoreRead]:
        result = await db_session.execute(select(StageScore))
        stage_scores = result.scalars().all()
        return stage_scores if stage_scores else []

    @staticmethod
    async def create(
        db_session: AsyncSession, stage_score: StageScoreCreate
    ) -> StageScoreRead:
        try:
            db_stage_score = StageScore(**stage_score.model_dump())
            db_session.add(db_stage_score)
            await db_session.commit()
            await db_session.refresh(db_stage_score)
            return db_stage_score
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to create stage score")

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, data: StageScoreUpdate
    ) -> Optional[StageScoreRead]:
        stage_score = await db_session.get(StageScore, id)
        if not stage_score:
            raise ValueError(f"Stage score with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(stage_score, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(stage_score)
            return stage_score
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update stage score")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        stage_score = await db_session.get(StageScore, id)
        if not stage_score:
            raise ValueError(f"Stage score with ID {id} not found")
        try:
            await db_session.delete(stage_score)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete stage score")
