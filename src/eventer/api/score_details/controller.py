from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import ScoreDetail
from .schema import ScoreDetailCreate, ScoreDetailRead, ScoreDetailUpdate


class ScoreDetailController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[ScoreDetailRead]:
        result = await db_session.execute(select(ScoreDetail).where(ScoreDetail.id == id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[ScoreDetailRead]:
        result = await db_session.execute(select(ScoreDetail))
        score_details = result.scalars().all()
        return score_details if score_details else []
    
    @staticmethod
    async def create(db_session: AsyncSession, score_detail: ScoreDetailCreate) -> ScoreDetailRead:
        try:
            db_score_detail = ScoreDetail(**score_detail.model_dump())
            db_session.add(db_score_detail)
            await db_session.commit()
            await db_session.refresh(db_score_detail)
            return db_score_detail
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to create score detail")
        
    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: ScoreDetailUpdate) -> Optional[ScoreDetailRead]:
        score_detail = await db_session.get(ScoreDetail, id)
        if not score_detail:
            raise ValueError(f"Score detail with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(score_detail, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(score_detail)
            return score_detail
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update score detail")
    
    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        score_detail = await db_session.get(ScoreDetail, id)
        if not score_detail:
            raise ValueError(f"Score detail with ID {id} not found")
        try:
            await db_session.delete(score_detail)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete score detail")