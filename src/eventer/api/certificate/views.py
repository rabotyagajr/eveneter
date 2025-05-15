from fastapi import APIRouter, HTTPException, status, Response, Depends
from .controller import CertificateController
from eventer.api.certificate.schema import (
    CertificateUpdate,
    CertificateCreate,
    CertificateRead,
)
from eventer.auth.auth import get_current_user
from typing import List
from eventer.database.database import DbSession
from sqlalchemy.exc import SQLAlchemyError

certificate_router = APIRouter(prefix="/certificates", tags=["Certificates"])


@certificate_router.get("/", response_model=List[CertificateRead])
async def get_certificates(db_session: DbSession):
    certificates = await CertificateController.get_all(db_session=db_session)
    return certificates


@certificate_router.get("/{id}", response_model=CertificateRead)
async def get_certificate_by_id(id: int, db_session: DbSession):
    certificate = await CertificateController.get_one(
        db_session=db_session, certificate_id=id
    )

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )

    return certificate


@certificate_router.patch(
    "/{id}", response_model=CertificateRead, status_code=status.HTTP_200_OK
)
async def patch_certificate(
    db_session: DbSession,
    id: int,
    data: CertificateUpdate,
    user: dict = Depends(get_current_user),
):
    try:
        result = await CertificateController.patch_certificate(
            db_session=db_session,
            certificate_id=id,
            certificate_data=data,
        )

        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )


@certificate_router.post(
    "/", response_model=CertificateRead, status_code=status.HTTP_201_CREATED
)
async def create_certificate(
    db_session: DbSession,
    data: CertificateCreate,
    user: dict = Depends(get_current_user),
):
    try:
        certificate = await CertificateController.create_certificate(
            db_session=db_session, certificate_data=data
        )
        return certificate
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )


@certificate_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
):
    certificate = await CertificateController.get_one(db_session, id)

    if certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    try:
        await CertificateController.delete_certificate(
            db_session=db_session, certificate=certificate
        )
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"detail": f"Certificate with id {id} deleted"},
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete certificate",
        )
