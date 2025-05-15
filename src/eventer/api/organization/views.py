from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.auth.auth import get_current_user
from eventer.database.database import DbSession
from .schema import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationRead,
)
from .controller import OrganizationController
from sqlalchemy.exc import SQLAlchemyError

organization_router = APIRouter(prefix="/organizations", tags=["Organizations"])


@organization_router.get("/", response_model=list[OrganizationRead])
async def get_all(db_session: DbSession) -> list[OrganizationRead]:
    organizations = await OrganizationController.get_all(db_session)
    return organizations


@organization_router.post("/", response_model=OrganizationRead)
async def create_organization(
    db_session: DbSession,
    data: OrganizationCreate,
    user: dict = Depends(get_current_user),
) -> OrganizationRead:
    try:
        organization = await OrganizationController.create(db_session, data)
        return organization
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@organization_router.get("/{id}", response_model=OrganizationRead)
async def get_organization(db_session: DbSession, id: int) -> OrganizationRead:
    result = await OrganizationController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return result


@organization_router.patch("/{id}", response_model=OrganizationRead)
async def update_organization(
    db_session: DbSession,
    id: int,
    data: OrganizationUpdate,
    user: dict = Depends(get_current_user),
) -> OrganizationRead:
    try:
        organization = await OrganizationController.update(db_session, id, data)
        return organization
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@organization_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await OrganizationController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
