from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import Team
from .schema import TeamCreate, TeamRead, TeamUpdate
from typing import Optional, List


class TeamController:

    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[TeamRead]:
        result = await db_session.execute(select(Team).where(Team.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[TeamRead]:
        result = await db_session.execute(select(Team))
        teams = result.scalars().all()
        return teams if teams else []

    @staticmethod
    async def create(db_session: AsyncSession, data: TeamCreate) -> Optional[TeamRead]:
        new_team = Team(**data.model_dump())
        db_session.add(data)
        try:
            await db_session.commit()
            await db_session.refresh(new_team)
            return new_team
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to create team")

    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: TeamUpdate) -> TeamRead:
        team = await db_session.get(Team, id)
        if not team:
            raise ValueError(f"Team with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(team, key, value)
        if not update_data:
            raise ValueError("No fields provided for update")

        try:
            await db_session.commit()
            await db_session.refresh(team)
            return team
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update team")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        team = await db_session.get(Team, id)
        if not team:
            raise ValueError(f"Team with ID {id} not found")
        try:
            await db_session.delete(team)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete team")
