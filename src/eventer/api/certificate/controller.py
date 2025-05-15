from eventer.models import Certificate
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import CertificateRead, CertificateCreate, CertificateUpdate
from sqlalchemy.exc import IntegrityError


class CertificateController:

    @staticmethod
    async def get_one(
        db_session: AsyncSession, certificate_id: int
    ) -> Optional[CertificateRead]:
        result = await db_session.execute(
            select(Certificate).where(Certificate.id == certificate_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[CertificateRead]:
        result = await db_session.execute(select(Certificate))
        certificates = result.scalars().all()
        return certificates if certificates else []

    @staticmethod
    async def patch_certificate(
        db_session: AsyncSession,
        certificate_id: int,
        certificate_data: CertificateUpdate,
    ) -> CertificateRead:
        certificate = await db_session.get(Certificate, certificate_id)

        if not certificate:
            raise ValueError(f"Certificate with ID {certificate_id} not found")
        update_data = certificate_data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValueError("No fields provided for update")

        for field, value in update_data.items():
            setattr(certificate, field, value)
        try:
            await db_session.commit()
            await db_session.refresh(certificate)
            return certificate

        except IntegrityError as e:
            await db_session.rollback()
            if "foreign key" in str(e).lower():
                raise ValueError("Invalid reference ID in update data")

    @staticmethod
    async def create_certificate(
        db_session: AsyncSession, certificate_data: CertificateCreate
    ) -> Optional[CertificateRead]:
        try:
            new_certificate = Certificate(
                file_path=certificate_data.file_path,
                type=certificate_data.type,
                user_id=certificate_data.user_id,
                event_id=certificate_data.event_id,
                stage_id=certificate_data.stage_id,
            )

            db_session.add(new_certificate)
            await db_session.commit()
            await db_session.refresh(new_certificate)

            return new_certificate
        except IntegrityError as e:
            await db_session.rollback()
            raise ValueError("invalid user_id, event_id or stage_id")

    @staticmethod
    async def delete_certificate(
        db_session: AsyncSession, certificate: Certificate
    ) -> None:
        await db_session.delete(certificate)
        await db_session.commit()
