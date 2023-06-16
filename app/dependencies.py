from typing_extensions import Annotated
from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import app.exceptions as exceptions
from app.db import db
from app.config.setting import Setting
from app.auth.schema import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def token_decode(token: Annotated[str, Depends(oauth2_scheme)]):
    
    try:
        payload = jwt.decode(token, Setting.SECRET_KEY, algorithms=[Setting.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get('role')
        expire: int = payload.get("exp")
        
        if username is None or role is None or expire is None:
            raise exceptions.credentials_exception_invalid
        elif role not in Setting.ROLE:
            raise exceptions.credentials_exception_invalid
        
        expire = datetime.fromtimestamp(expire)
        if expire < datetime.now(): # expired:
            raise exceptions.credentials_exception_expired
        
        token_data = TokenData(username=username,role=role,expire=expire)
        
    except JWTError:
        raise exceptions.credentials_exception_invalid

    return token_data

def check_permission(token_data: TokenData, tag:str, action:str):
    
    try:
        role = token_data.role
        
        if role not in Setting.PERMISSION[tag][action]:
            raise exceptions.permission_denied
        
    except KeyError:
        raise exceptions.permission_error
    
async def audit_log(username:str, action:str, message:str=''):
    
    await db["auditLog"].insert_one({
        'datetime': datetime.now(),
        "username": username,
        "action": action,
        "message": message
        })
    
# def formatted_datetime():
#     return datetime.now().strftime("%m/%d/%Y-%H:%M:%S")