from fastapi import HTTPException, status

credentials_exception_invalid = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception_expired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credentials expired",
    headers={"WWW-Authenticate": "Bearer"},
)

permission_denied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied"
)

permission_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Permission not set, implict denied"
)