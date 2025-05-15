from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import StageTeamTransition
from .schema import StageTeamTransitionCreate, StageTeamTransitionRead, StageTeamTransitionUpdate
from typing import Optional, List


class TeamController:

    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[StageTeamTransitionRead]:
        result = await db_session.execute(select(StageTeamTransition).where(StageTeamTransition.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[StageTeamTransitionRead]:
        result = await db_session.execute(select(StageTeamTransition))
        stage_team_transitions = result.scalars().all()
        return stage_team_transitions if stage_team_transitions else []

    @staticmethod
    async def create(db_session: AsyncSession, data: StageTeamTransitionCreate) -> Optional[StageTeamTransitionRead]:
        new_stage_team_transitions = StageTeamTransition(**data.model_dump())
        db_session.add(data)
        try:
            await db_session.commit()
            await db_session.refresh(new_stage_team_transitions)
            return new_stage_team_transitions
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to create stage team transitions")

    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: StageTeamTransitionUpdate) -> StageTeamTransitionUpdate:
        stage_team_transition = await db_session.get(stage_team_transition, id)
        if not stage_team_transition:
            raise ValueError(f"Stage team transitions with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stage_team_transition, key, value)
        if not update_data:
            raise ValueError("No fields provided for update")

        try:
            await db_session.commit()
            await db_session.refresh(stage_team_transition)
            return stage_team_transition
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update stage transitions team")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        stage_team_transitions = await db_session.get(stage_team_transitions, id)
        if not stage_team_transitions:
            raise ValueError(f"Stage team transitions with ID {id} not found")
        try:
            await db_session.delete(stage_team_transitions)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete team")
