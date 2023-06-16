from typing import List
from fastapi import Depends, APIRouter, HTTPException, status, Body
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.config.setting import Setting
from app.dependencies import token_decode, check_permission, audit_log
from app.crud.schema import Object1, Object1Create, Object1Update, Object1InDB
from app.crud.exceptions import field_duplicated_exception

router = APIRouter()

@router.post("/", response_description="Add new object1", response_model=Object1Create)
async def create_object1(object1: Object1Create = Body(...), auth = Depends(token_decode)):
    
    check_permission(auth,'test','full')
    
    object1 = jsonable_encoder(object1)
    
    if (await db["collection_name"].find_one({"field": object1["field"]})) is not None:
        raise field_duplicated_exception
    # or generate custom id for crud, oid will be used
    
    new_object = await db["collection_name"].insert_one(object1)
    created_object = await db["collection_name"].find_one({"_id": new_object.inserted_id})
    
    await audit_log(auth.username,'create','_msg_')
    return created_object


@router.get("/", response_description="List all object1", response_model=List[Object1])
async def list_object1(page: int = 0, auth = Depends(token_decode)):
    
    check_permission(auth,'test','full')
    
    object1 = await db["collection_name"].find().skip(
        page*Setting.PAGINATION_MAX_DOCS
        ).limit(
            Setting.PAGINATION_MAX_DOCS
            ).to_list(
                Setting.PAGINATION_MAX_DOCS
            )
    
    return object1


@router.get("/{field}", response_description="Get a single object1", response_model=Object1InDB)
async def show_object1(field: str, auth = Depends(token_decode)):
    
    check_permission(auth,'test','full')
    
    if (object1 := await db["collection_name"].find_one({"field": field})) is not None:
        return object1

    raise HTTPException(status_code=404, detail=f"object1 {field} not found")


@router.put("/{field}", response_description="Update a object1", response_model=Object1)
async def update_object1(field: str, object1: Object1Update = Body(...), auth = Depends(token_decode)):
    
    check_permission(auth,'test','full')
    
    object1 = {k: v for k, v in object1.dict().items() if v is not None}
    
    if object1['field'] != field:
        raise HTTPException(status_code=422,detail="field cannot be changed")

    if len(object1) >= 1:
        update_result = await db["collection_name"].update_one({"field": field}, {"$set": object1})
        
    if (updated_object1 := await db["collection_name"].find_one({"field": field})) is not None:
        return updated_object1
        
    await audit_log(auth.username,'update','_msg_')
    raise HTTPException(status_code=404, detail=f"object1 {field} not found")


@router.delete("/{field}", response_description="Delete a object1")
async def delete_object1(field: str, auth = Depends(token_decode)):
    
    check_permission(auth,'test','full')
    
    delete_result = await db["collection_name"].delete_one({"field": field})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    await audit_log(auth.username,'delete','_msg_')
    raise HTTPException(status_code=404, detail=f"object1 {field} not found")