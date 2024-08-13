from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from ngs_pipeline_lib.api.models import APISettings

settings = APISettings()

if settings.secure:
    oauth_2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=settings.keycloak_authorization_url,
        tokenUrl=settings.keycloak_token_url,
        refreshUrl=settings.keycloak_refresh_url,
    )
else:
    oauth_2_scheme = None


def valid_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = settings.keycloak_certs_url
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = jwt.PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")
