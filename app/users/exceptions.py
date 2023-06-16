from fastapi import HTTPException, status

same_username_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists",
)