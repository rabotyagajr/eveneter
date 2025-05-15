from eventer.models import EventDay
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from .schema import EventDayCreate, EventDayRead, EventDayUpdate
from sqlalchemy import select


class EventDayController:
    @staticmethod
    async def get_one(
        db_session: AsyncSession,
        id: int,
    ) -> Optional[EventDayRead]:
        result = await db_session.execute(select(EventDay).where(EventDay.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[EventDayRead]:
        result = await db_session.execute(select(EventDay))
        event_days = result.scalars().all()        
        return event_days if event_days else []
    
    @staticmethod
    async def create(db_session: AsyncSession, data: EventDayCreate) -> EventDay:
        try:
            new_event_day = EventDay(
                start_time = data.start_time,
                end_time = data.end_time,
            )
            db_session.add(new_event_day)
            await db_session.commit()
            await db_session.refresh(new_event_day)
            return new_event_day
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def update(
        db_session: AsyncSession,
        id: int,
        data: EventDayUpdate
    ) -> Optional[EventDay]:
        event_day = await db_session.get(EventDay, id)
        if not event_day:
            raise ValueError(f"EventDay with ID {id} not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(event_day, key, value)

        try:
            await db_session.commit()
            await db_session.refresh(event_day)
            return event_day
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        event_day = await db_session.get(EventDay, id)
        if not event_day:
            raise ValueError(f"EventDay with ID {id} not found")
        await db_session.delete(event_day)
        await db_session.commit()