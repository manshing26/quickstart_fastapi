from typing import List
from fastapi import Depends, APIRouter, HTTPException, status, Body
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.config.setting import Setting
from app.dependencies import token_decode, check_permission, audit_log
from app.users.dependencies import get_user_from_db
from app.users.schema import User, UserUpdate, AdminUserCreate, AdminUserUpdate, UserInDB
from app.users.exceptions import same_username_exception

router = APIRouter()
pwd_context = Setting.pwd_context

@router.get("/me/", response_description="Get myself", response_model=User)
async def show_myself(auth = Depends(token_decode)):
    
    check_permission(auth,'users','show_myself')
    
    user = await get_user_from_db(username=auth.username)
    
    return user


@router.put("/me/", response_description="Update myself", response_model=User)
async def update_myself(user: UserUpdate = Body(...), auth = Depends(token_decode)):
    
    check_permission(auth,'users','update_myself')
    
    user = {key: value for key, value in user.dict().items() if value is not None}
    
    if user['username'] != auth.username:
        raise HTTPException(status_code=422,detail="username cannot be changed")
    if user.get('hashed_password') != None:
        user['hashed_password'] = pwd_context.hash(user['hashed_password'])

    if len(user) >= 1:
        update_result = await db["users"].update_one({"username": auth.username}, {"$set": user})

    updated_user = await get_user_from_db(username=auth.username)
    
    await audit_log(auth.username, 'Update self profile', f'Data: {user}')
    return updated_user


@router.get("/", response_description="List all users", response_model=List[User])
async def list_users(auth = Depends(token_decode)):
    
    check_permission(auth,'users','list_users')
    
    users = await db["users"].find().to_list(1000)
    return users


@router.get("/{username}", response_description="Get a single user", response_model=User)
async def show_user(username: str, auth = Depends(token_decode)):
    
    check_permission(auth,'users','show_user')
    
    user = await get_user_from_db(username=username)
    return user


@router.get("/admin/", response_description="List all users (detail)", response_model=List[UserInDB])
async def admin_list_users(auth = Depends(token_decode)):
    
    check_permission(auth,'users','admin_only')
    
    users = await db["users"].find().to_list(1000)
    return users


@router.post("/admin/", response_description="Create a normal user", response_model=AdminUserCreate)
async def admin_create_user(user: AdminUserCreate = Body(...), auth = Depends(token_decode)):
    
    check_permission(auth,'users','admin_only')
    
    user = jsonable_encoder(user)
    
    if (await db["users"].find_one({"username": user["username"]})) is not None:
        raise same_username_exception
    if user['role'] not in Setting.ROLE:
        raise HTTPException(status_code=422,detail="Role is not defined")

    user['hashed_password'] = pwd_context.hash(user['hashed_password'])
    # user['active'] = True
    # user['role'] = 'user'
    
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    
    await audit_log(auth.username, 'Create user', f'Created: {user["username"]}')
    return created_user


@router.get("/admin/{username}", response_description="Get a single user (detail)", response_model=UserInDB)
async def admin_show_user(username: str, auth = Depends(token_decode)):
    
    check_permission(auth,'users','admin_only')
    
    user = await get_user_from_db(username=username)
    return user


@router.put("/admin/{username}", response_description="Update an user", response_model=AdminUserUpdate)
async def admin_update_user(username: str, user: AdminUserUpdate = Body(...), auth = Depends(token_decode)):
    
    check_permission(auth,'users','admin_only')
    
    user = {key: value for key, value in user.dict().items() if value is not None}
    
    if user['username'] != username:
        raise HTTPException(status_code=422,detail="Username cannot be changed")
    if user['role'] not in Setting.ROLE:
        raise HTTPException(status_code=422,detail="Role is not defined")
    
    if user.get('hashed_password') != None:
        user['hashed_password'] = pwd_context.hash(user['hashed_password'])

    if len(user) >= 1:
        update_result = await db["users"].update_one({"username": username}, {"$set": user})

    #     if update_result.modified_count == 1:
    #         if (
    #             updated_user := await db["users"].find_one({"username": username})
    #         ) is not None:
    #             return updated_user
    
    updated_user = await get_user_from_db(username=username)
    
    await audit_log(auth.username, 'Update an user profile', f'Data: {user}')
    return updated_user


@router.delete("/admin/{username}", response_description="Delete an user")
async def admin_delete_user(username: str, auth = Depends(token_decode)):
    
    check_permission(auth,'users','admin_only')
        
    delete_result = await db["users"].delete_one({"username": username})

    if delete_result.deleted_count == 1:
        audit_log(auth.username, 'Delete an user', f'Deleted: {username}')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Username {username} not found")

