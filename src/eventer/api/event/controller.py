from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException
from fastapi import UploadFile
from eventer.enums import Status
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import Event
from eventer.storage.repository import MinioRepository
from .schema import EventCreate, EventRead, EventUpdate, EventRecent
from datetime import datetime


class EventController:

    @staticmethod
    async def get_recents(
        db_session: AsyncSession, limit: int
    ) -> Optional[list[EventRecent]]:
        try:
            result = await db_session.execute(
                select(Event)
                .where(Event.event_status == Status.ACTIVE)
                .where(Event.start_date > datetime.now())
                .order_by(Event.start_date.asc())
                .limit(limit)
            )

            if result is None:
                return []

            events = result.scalars().all()

            return events

        except HTTPException as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail="Failed to get recent events")

    @staticmethod
    async def get(db_session: AsyncSession, id: int) -> Optional[EventRead]:
        result = await db_session.execute(select(Event).where(Event.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[EventRead]:
        result = await db_session.execute(select(Event))
        events = result.scalars().all()
        return events if events else []

    @staticmethod
    async def create(db_session: AsyncSession, data: EventCreate) -> EventRead:
        new_event = Event(**data.model_dump())
        db_session.add(new_event)
        try:
            await db_session.commit()
            await db_session.refresh(new_event)
            return new_event
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError(f"Failed to create event {e}")

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, data: EventUpdate
    ) -> Optional[EventRead]:
        event = await db_session.get(Event, id)
        if not event:
            raise ValueError(f"Event with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(event, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(event)
            return event
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update event")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        event = await db_session.get(Event, id)
        if not event:
            raise ValueError(f"Event with ID {id} not found")
        try:
            await db_session.delete(event)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete event")

    @staticmethod
    async def upload_image(
        db_session: AsyncSession,
        event_id: int,
        file: UploadFile,
        minio_repo: MinioRepository,
    ) -> None:
        event = await db_session.get(Event, event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")
        try:
            event.image_url = await minio_repo.upload(event_id, file)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError(f"Failed to upload image {e}")

    @staticmethod
    async def get_image(
        db_session: AsyncSession,
        event_id: int,
        minio_repo: MinioRepository,
    ) -> BytesIO:
        event = await db_session.get(Event, event_id)
        if not event or not event.image_url:
            raise ValueError("Image not found")
        
        fileobj = minio_repo.download(event.image_url)
        
        content_bytes = fileobj.getvalue()
        
        return event.image_url, content_bytes