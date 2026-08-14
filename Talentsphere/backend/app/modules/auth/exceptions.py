from fastapi import HTTPException, status

class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AccountLockedException(HTTPException):
    def __init__(self, detail: str = "Account is locked or suspended. Please contact support."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class UserInactiveException(HTTPException):
    def __init__(self, detail: str = "Account is disabled or pending verification"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class TokenExpiredException(HTTPException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class TokenRevokedException(HTTPException):
    def __init__(self, detail: str = "Session or token has been revoked"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class InvalidTokenException(HTTPException):
    def __init__(self, detail: str = "Could not validate authentication credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedException(HTTPException):
    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class RoleDeniedException(HTTPException):
    def __init__(self, detail: str = "Required role missing"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class TenantAccessDeniedException(HTTPException):
    def __init__(self, detail: str = "Cross-tenant access violation detected"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class PasswordPolicyException(HTTPException):
    def __init__(self, detail: str = "Password does not meet complexity requirements"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
