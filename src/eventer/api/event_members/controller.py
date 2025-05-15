from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import EventMember
from .schema import EventMemberCreate, EventMemberRead, EventMemberUpdate

class EventMemberController:
    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[EventMemberRead]:
        result = await db_session.execute(select(EventMember).where(EventMember.id == id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[EventMemberRead]:
        result = await db_session.execute(select(EventMember))
        event_members = result.scalars().all()
        return event_members if event_members else []
    
    @staticmethod
    async def create(db_session: AsyncSession, event_member: EventMemberCreate) -> EventMemberRead:
        try:
            db_event_member = EventMember(**event_member.model_dump())
            db_session.add(db_event_member)
            await db_session.commit()
            await db_session.refresh(db_event_member)
            return db_event_member
        except SQLAlchemyError as e:
            raise SQLAlchemyError("Failed to create event member")
        
    @staticmethod
    async def update(db_session: AsyncSession, id: int, data: EventMemberUpdate) -> Optional[EventMemberRead]:
        event_member = await db_session.get(EventMember, id)
        if not event_member:
            raise ValueError(f"Event member with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(event_member, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(event_member)
            return event_member
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update event member")
        
    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        event_member = await db_session.get(EventMember, id)    
        if not event_member:
            raise ValueError(f"Event member with ID {id} not found")
        try:
            await db_session.delete(event_member)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete event member")