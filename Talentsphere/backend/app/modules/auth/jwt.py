import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel
from app.core.config import settings
from app.modules.auth.exceptions import TokenExpiredException, InvalidTokenException
from app.modules.auth.security import generate_random_token, hash_token

class TokenPayload(BaseModel):
    sub: str # user_id
    org_id: Optional[str] = None # organization_id
    account_type: str
    jti: str # JWT Token ID
    exp: datetime
    type: str = "access"

def create_access_token(
    user_id: str | uuid.UUID,
    organization_id: Optional[str | uuid.UUID],
    account_type: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Generates a signed JWT access token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "org_id": str(organization_id) if organization_id else None,
        "account_type": account_type,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": expire,
        "type": "access"
    }

    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token() -> tuple[str, str]:
    """
    Generates a cryptographically secure raw refresh token and its SHA-256 hash.
    Returns: (raw_refresh_token, token_hash)
    """
    raw_token = generate_random_token(64)
    token_hash_str = hash_token(raw_token)
    return raw_token, token_hash_str

def decode_access_token(token: str) -> TokenPayload:
    """Decodes and validates a signed JWT access token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        token_type = payload.get("type")
        if token_type != "access":
            raise InvalidTokenException("Invalid token type")
            
        sub: str = payload.get("sub")
        org_id: Optional[str] = payload.get("org_id")
        account_type: str = payload.get("account_type")
        jti: str = payload.get("jti")
        exp_timestamp = payload.get("exp")
        
        if not sub:
            raise InvalidTokenException("Token payload incomplete")
            
        exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        if exp < datetime.now(timezone.utc):
            raise TokenExpiredException()
            
        return TokenPayload(
            sub=sub,
            org_id=org_id,
            account_type=account_type or "RECRUITER",
            jti=jti or str(uuid.uuid4()),
            exp=exp,
            type="access"
        )
    except JWTError:
        raise InvalidTokenException("Could not decode access token")
