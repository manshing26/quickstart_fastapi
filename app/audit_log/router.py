from typing import List
from datetime import datetime, date
from fastapi import Depends, APIRouter

from app.db import db
from app.config.setting import Setting
from app.dependencies import token_decode, check_permission
from app.audit_log.schema import AuditLogInDB

router = APIRouter()

@router.get("/", response_description="Check audit log", response_model = List[AuditLogInDB])
async def audit_log_query(
    page: int = 0,
    username: str = None,
    action: str = None,
    date_from: date = None,
    date_to: date = None,
    date_descending: bool = True,
    auth = Depends(token_decode)
    ):
    check_permission(auth,'audit_log','query')
        
    query_filter = {}
    if username != None:
        query_filter['username'] = username
        
    if action != None:
        query_filter['action'] = action
        
    if (date_from != None) or (date_to != None):
        
        query_filter["datetime"] = {}
        
        if date_from != None:
            datetime_from = datetime(
                date_from.year,
                date_from.month,
                date_from.day,
            )
            query_filter["datetime"]['$gte'] = datetime_from
            
        if date_to != None:
            datetime_to = datetime(
                date_to.year,
                date_to.month,
                date_to.day,
                23,59,59
            )
            query_filter["datetime"]['$lte'] = datetime_to
            
    sort_int = -1
    if not date_descending:
        sort_int = 1
                
    log_list = await db["auditLog"].find(query_filter).sort('datetime',sort_int).skip(
        page*Setting.PAGINATION_MAX_DOCS).limit(Setting.PAGINATION_MAX_DOCS).to_list(
            Setting.PAGINATION_MAX_DOCS)
    
    return log_list