from pydantic import BaseSettings, Field


class APISettings(BaseSettings):
    secure: bool = Field(default=False, env="API_SECURE")
    root_path: str | None = Field(default=None, env="API_ROOT_PATH")
    prefix_path: str = Field(default="", env="API_PREFIX_PATH")

    keycloak_authorization_url: str | None = None
    keycloak_token_url: str | None = None
    keycloak_refresh_url: str | None = None
    keycloak_certs_url: str | None = None
