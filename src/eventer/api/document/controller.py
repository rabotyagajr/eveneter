from typing import List, Optional
from eventer.models import Document
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import DocumentRead, DocumentCreate, DocumentUpdate


class DocumnetController:

    @staticmethod
    async def get_one(db_session: AsyncSession, id: int) -> Optional[DocumentRead]:
        result = await db_session.execute(select(Document).where(Document.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[DocumentRead]:
        result = await db_session.execute(select(Document))
        documents = result.scalars().all()
        return documents if documents else []

    @staticmethod
    async def create(db_session: AsyncSession, data: DocumentCreate) -> DocumentRead:
        new_document = Document(**data.model_dump())
        try:
            db_session.add(new_document)
            await db_session.commit()
            await db_session.refresh(new_document)
            return new_document
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, data: DocumentUpdate
    ) -> DocumentRead:
        document = await db_session.get(Document, id)
        if not document:
            raise ValueError(f"Document with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update")
        for key, value in update_data.items():
            setattr(document, key, value)
        try:
            await db_session.commit()
            await db_session.refresh(document)
            return document
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        document = await db_session.get(Document, id)
        if not document:
            raise ValueError(f"Document with ID {id} not found")
        try:
            await db_session.delete(document)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete user")
