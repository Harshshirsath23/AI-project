import json
from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from app.config.settings import get_settings

settings = get_settings()


class TokenPayload:
    """JWT token payload structure."""

    def __init__(
        self,
        sub: str,  # user_id
        email: str,
        organization_id: str,
        role_id: str,
        token_type: str,  # access or refresh
        exp: datetime,
        iat: datetime,
        jti: str,  # JWT ID for token rotation
    ):
        self.sub = sub
        self.email = email
        self.organization_id = organization_id
        self.role_id = role_id
        self.token_type = token_type
        self.exp = exp
        self.iat = iat
        self.jti = jti


def create_access_token(
    user_id: str,
    email: str,
    organization_id: str,
    role_id: str,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, datetime]:
    """
    Create an access token.
    
    Returns:
        tuple: (token, expiration_datetime)
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    now = datetime.utcnow()
    jti = f"{user_id}-{int(now.timestamp())}"
    
    to_encode = {
        "sub": user_id,
        "email": email,
        "organization_id": organization_id,
        "role_id": role_id,
        "token_type": "access",
        "exp": expire,
        "iat": now,
        "jti": jti,
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    
    return encoded_jwt, expire


def create_refresh_token(
    user_id: str,
    email: str,
    organization_id: str,
    role_id: str,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, datetime]:
    """
    Create a refresh token.
    
    Returns:
        tuple: (token, expiration_datetime)
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Refresh tokens last longer (7 days by default)
        expire = datetime.utcnow() + timedelta(days=7)
    
    now = datetime.utcnow()
    jti = f"{user_id}-refresh-{int(now.timestamp())}"
    
    to_encode = {
        "sub": user_id,
        "email": email,
        "organization_id": organization_id,
        "role_id": role_id,
        "token_type": "refresh",
        "exp": expire,
        "iat": now,
        "jti": jti,
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    
    return encoded_jwt, expire


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Decode and validate a JWT token.
    
    Returns:
        TokenPayload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        
        return TokenPayload(
            sub=payload.get("sub"),
            email=payload.get("email"),
            organization_id=payload.get("organization_id"),
            role_id=payload.get("role_id"),
            token_type=payload.get("token_type"),
            exp=datetime.fromtimestamp(payload.get("exp")),
            iat=datetime.fromtimestamp(payload.get("iat")),
            jti=payload.get("jti"),
        )
    except JWTError:
        return None


def verify_token_type(token: str, expected_type: str) -> bool:
    """
    Verify that a token is of the expected type (access or refresh).
    
    Returns:
        bool: True if token type matches, False otherwise
    """
    payload = decode_token(token)
    if not payload:
        return False
    
    return payload.token_type == expected_type


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration datetime of a token.
    
    Returns:
        datetime if valid, None otherwise
    """
    payload = decode_token(token)
    if not payload:
        return None
    
    return payload.exp


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired.
    
    Returns:
        bool: True if expired, False otherwise
    """
    payload = decode_token(token)
    if not payload:
        return True
    
    return datetime.utcnow() > payload.exp
