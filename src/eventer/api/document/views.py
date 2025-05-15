from typing import List
from eventer.database.database import DbSession
from fastapi import APIRouter, status, HTTPException, Response, Depends
from eventer.auth.auth import get_current_user
from .schema import DocumentCreate, DocumentUpdate, DocumentRead
from .controller import DocumnetController
from sqlalchemy.exc import SQLAlchemyError

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.get("/", response_model=list[DocumentRead])
async def get_all(db_session: DbSession) -> List[DocumentRead]:
    documents = await DocumnetController.get_all(db_session)
    return documents


@document_router.get("/{id}", response_model=DocumentRead)
async def get_document(db_session: DbSession, id: int) -> DocumentRead:
    document = await DocumnetController.get_one(db_session, id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return document


@document_router.patch("/{id}", response_model=DocumentRead)
async def update_document(
    db_session: DbSession,
    id: int,
    data: DocumentUpdate,
    user: dict = Depends(get_current_user),
) -> DocumentRead:
    try:
        document = await DocumnetController.update(db_session, id, data)
        return document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@document_router.post("/", response_model=DocumentRead)
async def create_document(
    db_session: DbSession, data: DocumentCreate, user: dict = Depends(get_current_user)
) -> DocumentRead:
    try:
        document = await DocumnetController.create(db_session, data)
        return document
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@document_router.delete("/{id}")
async def delete_document(
    db_session: DbSession, id: int, user: dict = Depends(get_current_user)
) -> None:
    try:
        await DocumnetController.delete(db_session, id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            content=f"Document with id {id} deleted",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
