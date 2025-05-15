from fastapi.security import OAuth2AuthorizationCodeBearer
from eventer.core.config import settings
from typing import Annotated
from keycloak import KeycloakOpenID, KeycloakAuthenticationError
from fastapi import HTTPException, status, Depends

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.keycloak_cfg.server_url}realms/{settings.keycloak_cfg.realm_name}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.keycloak_cfg.server_url}realms/{settings.keycloak_cfg.realm_name}/protocol/openid-connect/token",
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.keycloak_cfg.server_url,
    client_id=settings.keycloak_cfg.client_id,
    realm_name=settings.keycloak_cfg.realm_name,
    client_secret_key=settings.keycloak_cfg.client_secret_key,
    verify=True,
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_info = await keycloak_openid.a_introspect(token)
        if not token_info.get("active"):
            raise HTTPException(status_code=401, detail="Invalid token")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_access_token(username: str, password: str) -> str:
    try:
        token = keycloak_openid.token(username, password)
        return token["access_token"]
    except KeycloakAuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


# RBAC
def require_role(
    required_realm_roles: list[str] = None,
    required_client_roles: list[str] = None,
    client: str = "account",
):
    """
    Dependency для проверки наличия хотя бы одной из требуемых ролей у пользователя
    Args:
        required_realm_roles: список требуемых ролей в реалме
        required_client_roles: список требуемых ролей в клиенте
        client: название клиента
    """

    async def role_checker(user: dict = Depends(get_current_user)):
        if required_realm_roles:
            user_realm_roles = user.get("realm_access", {}).get("roles", [])

            if not any(role in user_realm_roles for role in required_realm_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )

        if required_client_roles:
            user_client_roles = (
                user.get("resource_access", {})
                .get(client, {})
                .get("roles", [])
            )
            if not any(role in user_client_roles for role in required_client_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )

        return user

    return role_checker
