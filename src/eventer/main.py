from fastapi import FastAPI, Depends
import uvicorn
from eventer.database.database import create_tables
import asyncio
from eventer.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from eventer.auth.auth import get_current_user, require_role

app = FastAPI(
    title="API c Keycloak Auth",
    redoc_url="/redoc",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/me", summary="Получить информацию о пользователе + RBAC")
async def protected_with_role(
    user: dict = Depends(get_current_user),
    _: bool = Depends(require_role(required_client_roles=["organizer"])),
):
    return {"user_info": user}


if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
