from fastapi import HTTPException, status

field_duplicated_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Unique/Key field duplicated",
)