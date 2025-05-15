from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from .paths import ROOT_DIR


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="MINIO_",
    )

    endpoint: str = Field(..., env="ENDPOINT")
    access_key: str = Field(..., env="ACCESS_KEY")
    secret_key: str = Field(..., env="SECRET_KEY")
    bucket: str = Field(..., env="BUCKET")
    secure: bool = Field(..., env="SECURE")


class KeyCloakSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="KEYCLOAK_",
    )

    server_url: str = Field(..., env="SERVER_URL")
    client_id: str = Field(..., env="CLIENT_ID")
    realm_name: str = Field(..., env="REALM_NAME")
    client_secret_key: str = Field(..., env="CLIENT_SECRET_KEY")


class Settings(BaseSettings):

    keycloak_cfg: KeyCloakSettings = KeyCloakSettings()
    minio_cfg: MinioSettings = MinioSettings()

    db_uri: str = "postgresql+asyncpg://postgres:root@localhost:5432/eventer"
    db_echo: bool = True


settings = Settings()
