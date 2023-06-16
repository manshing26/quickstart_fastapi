from fastapi import HTTPException

from app.db import db

async def get_user_from_db(username: str):
    
    if (user := await db["users"].find_one({"username": username})) is not None:
        return user
    
    raise HTTPException(status_code=404, detail=f"Username {username} not found")

async def get_user_from_db_active(username: str):
    
    user = await get_user_from_db(username=username)
    
    if user['active'] == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user
