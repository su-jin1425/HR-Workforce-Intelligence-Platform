from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import Settings, get_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_access_token(subject: str, role: str, settings: Settings | None = None) -> str:
    active_settings = settings or get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=active_settings.access_token_minutes)
    claims = {"sub": subject, "role": role, "exp": expires_at}
    return jwt.encode(claims, active_settings.secret_key, algorithm="HS256")


async def require_api_principal(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer),
    settings: Settings = Depends(get_settings),
) -> dict[str, Any]:
    if not settings.require_plugin_auth:
        return {"sub": "local-dev", "role": "hr_admin"}
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token") from exc
    return payload
