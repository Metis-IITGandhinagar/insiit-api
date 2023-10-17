from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from config import api_config

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
api_keys: list = api_config["api-keys"]


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing headers: x-api-key"
        )
    if api_key_header in api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
