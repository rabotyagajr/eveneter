from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from eventer.models import Organization
from .schema import OrganizationCreate, OrganizationRead, OrganizationUpdate


class OrganizationController:
    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[OrganizationRead]:
        organizations = await db_session.execute(select(Organization))
        organizations = organizations.scalars().all()
        return organizations if organizations else []

    @staticmethod
    async def get(
        db_session: AsyncSession, organization_id: int
    ) -> Optional[OrganizationRead]:
        result = await db_session.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db_session: AsyncSession, data: OrganizationCreate
    ) -> OrganizationRead:
        new_organization = Organization(**data.model_dump())
        db_session.add(new_organization)
        try:
            await db_session.commit()
            await db_session.refresh(new_organization)
            return new_organization
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to create organization")

    @staticmethod
    async def update(
        db_session: AsyncSession, id: int, data: OrganizationUpdate
    ) -> OrganizationRead:
        organization = await db_session.get(Organization, id)
        if not organization:
            raise ValueError(f"Organization with ID {id} not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(organization, key, value)

        if not update_data:
            raise ValueError("No fields provided for update")

        try:
            await db_session.commit()
            await db_session.refresh(organization)
            return organization
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to update organization")

    @staticmethod
    async def delete(db_session: AsyncSession, id: int) -> None:
        organization = await db_session.get(Organization, id)
        if not organization:
            raise ValueError(f"Organization with ID {id} not found")
        try:
            await db_session.delete(organization)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise SQLAlchemyError("Failed to delete organization")
