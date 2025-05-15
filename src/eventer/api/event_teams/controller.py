from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import EventTeam
from .schema import EventTeamCreate, EventTeamRead, EventTeamUpdate

class EventTeamController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[EventTeamRead]:
        result = await db_session.execute(select(EventTeam).where(EventTeam.id == id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[EventTeamRead]:
        result = await db_session.execute(select(EventTeam))
        event_teams = result.scalars().all()
        return event_teams if event_teams else []
    
    @staticmethod
    async def create(db_session: AsyncSession, event_team: EventTeamCreate) -> EventTeamRead:
        try:
            db_event_team = EventTeam(**event_team.model_dump())
            db_session.add(db_event_team)
            await db_session.commit()
            await db_session.refresh(db_event_team)
            return db_event_team
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to create event team")
    
    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: EventTeamUpdate) -> Optional[EventTeamRead]:
        event_team = await db_session.get(EventTeam, id)
        if not event_team:
            raise ValueError(f"Event team with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(event_team, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(event_team)
            return event_team
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update event team")
    
    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        event_team = await db_session.get(EventTeam, id)
        if not event_team:
            raise ValueError(f"Event team with ID {id} not found")
        try:
            await db_session.delete(event_team)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete event team")