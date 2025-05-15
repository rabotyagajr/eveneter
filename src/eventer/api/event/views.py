from fastapi import APIRouter, HTTPException, status, Response, Depends
from eventer.database.database import DbSession
from .schema import EventUpdate, EventCreate, EventRead, EventRecent
from .controller import EventController
from fastapi import UploadFile, Query
from sqlalchemy.exc import SQLAlchemyError
from eventer.storage.repository import MinioRepository, get_minio_repo
from eventer.auth.auth import get_current_user

event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.get("/", response_model=list[EventRead])
async def get_all(db_session: DbSession) -> list[EventRead]:
    return await EventController.get_all(db_session)


@event_router.get("/{id}/", response_model=EventRead)
async def get(db_session: DbSession, id: int) -> EventRead:
    result = await EventController.get(db_session, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return result


@event_router.post("/", response_model=EventRead)
async def create(
    db_session: DbSession, data: EventCreate, user: dict = Depends(get_current_user)
) -> EventRead:
    try:
        result = await EventController.create(db_session, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_router.patch("/{id}/", response_model=EventRead)
async def update(
    db_session: DbSession,
    id: int,
    data: EventUpdate,
    user: dict = Depends(get_current_user),
) -> EventRead:
    try:
        result = await EventController.update(db_session, id, data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await EventController.delete(db_session, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_router.get("/recent", response_model=list[EventRecent])
async def get_recent(db_session: DbSession, limit: int = Query(default=5)) -> list[EventRecent]:
    return await EventController.get_recents(db_session, limit)


@event_router.post("/{event_id}/upload-image/", status_code=status.HTTP_201_CREATED)
async def upload_image(
    db_session: DbSession,
    event_id: int,
    file: UploadFile,
    minio_repo: MinioRepository = Depends(get_minio_repo),
    user: dict = Depends(get_current_user),
):
    try:
        await EventController.upload_image(
            db_session, event_id=event_id, file=file, minio_repo=minio_repo
        )
        return Response(status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@event_router.get("/{event_id}/image/", status_code=status.HTTP_200_OK)
async def get_image(
    db_session: DbSession,
    event_id: int,
    minio_repo: MinioRepository = Depends(get_minio_repo),
):
    try:
        filename, content_bytes = await EventController.get_image(
            db_session=db_session, event_id=event_id, minio_repo=minio_repo
        )
        
        
        return Response(
            content=content_bytes,
            media_type="image/webp",
            headers={
                "Content-Disposition": f'inline; filename="{filename.split("/")[-1]}"'
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
