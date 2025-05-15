from typing import List, Optional
from eventer.models import TeamMember
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import TeamMemberRead, TeamMemberCreate, TeamMemberUpdate


class TeamMemberController:

    @staticmethod
    async def get_one(
        db_session: AsyncSession, user_id: int, team_id: int
    ) -> Optional[TeamMemberRead]:
        result = await db_session.execute(
            select(TeamMember).where(
                TeamMember.team_id == team_id, TeamMember.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[TeamMemberRead]:
        result = await db_session.execute(select(TeamMember))
        team_members = result.scalars().all()
        return team_members if team_members else []

    @staticmethod
    async def get_all_by_team(
        db_session: AsyncSession, team_id: int
    ) -> List[TeamMemberRead]:
        result = await db_session.execute(
            select(TeamMember).where(TeamMember.team_id == team_id)
        )
        team_members = result.scalars().all()
        return team_members if team_members else []

    @staticmethod
    async def get_all_by_user(
        db_session: AsyncSession, user_id: int
    ) -> List[TeamMemberRead]:
        result = await db_session.execute(
            select(TeamMember).where(TeamMember.user_id == user_id)
        )
        team_members = result.scalars().all()
        return team_members if team_members else []

    @staticmethod
    async def create(
        db_session: AsyncSession, data: TeamMemberCreate
    ) -> TeamMemberRead:
        new_team_member = TeamMember(**data.model_dump())
        try:
            db_session.add(new_team_member)
            await db_session.commit()
            await db_session.refresh(new_team_member)
            return new_team_member
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def update(
        db_session: AsyncSession, user_id: int, team_id: int, data: TeamMemberUpdate
    ) -> TeamMemberRead:
        team_member = await db_session.get(TeamMember, team_id, user_id)
        if not team_member:
            raise ValueError(f"Team member with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(team_member, key, value)
        if update_data:
            raise ValueError("No fields provided for update")
        try:
            await db_session.commit()
            await db_session.refresh(team_member)
            return team_member
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update team member")

    @staticmethod
    async def delete(db_session: AsyncSession, user_id: int, team_id: int) -> None:
        team_member = await db_session.get(TeamMember, user_id, team_id)
        if not team_member:
            raise ValueError(f"Team member with ID {id} not found")
        try:
            await db_session.delete(team_member)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete team member")
