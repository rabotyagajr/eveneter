from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import LeaderBoard
from .schema import LeaderBoardCreate, LeaderBoardRead, LeaderBoardUpdate


class LeaderBoardController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[LeaderBoardRead]:
        result = await db_session.execute(
            select(LeaderBoard).where(LeaderBoard.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[LeaderBoardRead]:
        result = await db_session.execute(select(LeaderBoard))
        leaderboards = result.scalars().all()
        return leaderboards if leaderboards else []

    @staticmethod
    async def create(db_session: AsyncSession, data: LeaderBoardCreate) -> LeaderBoardRead:
        new_leaderboard = LeaderBoard(**data.model_dump())
        try:
            db_session.add(new_leaderboard)
            await db_session.commit()
            await db_session.refresh(new_leaderboard)
            return new_leaderboard
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to create leaderboard")
        
    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: LeaderBoardUpdate) -> LeaderBoardRead:
        leaderboard = await db_session.get(LeaderBoard, id)
        if not leaderboard:
            raise ValueError(f"Leaderboard with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(leaderboard, key, value)
        if update_data:
            raise ValueError("No fields provided for update")
        try:
            await db_session.commit()
            await db_session.refresh(leaderboard)
            return leaderboard
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update leaderboard")
        
    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        leaderboard = await db_session.get(LeaderBoard, id)
        if not leaderboard:
            raise ValueError(f"Leaderboard with ID {id} not found")
        try:
            await db_session.delete(leaderboard)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete leaderboard")