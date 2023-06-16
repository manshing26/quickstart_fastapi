from bson import ObjectId
from typing import Union, Optional
from pydantic import BaseModel, Field, EmailStr

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    username: str
    email: Union[EmailStr, None] = None
    phone: Union[int,None] = None
    full_name: Union[str, None] = None
    
    # class Config:
    #     schema_extra = {}

class UserUpdate(User):
    email: Optional[EmailStr]
    phone: Optional[int]
    full_name: Optional[str]
    hashed_password: Optional[str]
    
class AdminUserCreate(User):
    role: str = 'user'
    hashed_password: str
    active: bool = True

class AdminUserUpdate(User):
    email: Optional[EmailStr]
    phone: Optional[int]
    full_name: Optional[str]
    hashed_password: Optional[str]
    role: Optional[str] = 'user'
    active: Optional[bool] = True

class UserInDB(User):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    role: str
    hashed_password: str
    active: bool
    
    class Config: # Must need for id
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}