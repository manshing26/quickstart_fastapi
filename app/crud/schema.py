from bson import ObjectId
from typing import Union, Optional
from pydantic import BaseModel, Field

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

class Object1(BaseModel): # no Id
    field: str
    field_int: Union[int,None] = None
    field_str: Union[str, None] = None
        
class Object1Create(Object1):
    prohibited_field_str: str = 'default'
    prohibited_field_int: int = 1

class Object1Update(Object1):
    field: Optional[str]
    field_int: Optional[int] = None
    field_str: Optional[str] = None
    prohibited_field_str: Optional[str] = 'default'
    prohibited_field_int: Optional[int] = 1

class Object1InDB(Object1):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    field: str
    field_int: int
    field_str: str
    prohibited_field_str: str
    prohibited_field_int: int

    
    class Config: # Must need for id
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
# class StudentModel(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     name: str = Field(...)
#     email: EmailStr = Field(...)
#     course: str = Field(...)
#     gpa: float = Field(..., le=4.0)

#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "name": "Jane Doe",
#                 "email": "jdoe@example.com",
#                 "course": "Experiments, Science, and Fashion in Nanophotonics",
#                 "gpa": "3.0",
#             }
#         }

# class UpdateStudentModel(BaseModel):
#     name: Optional[str]
#     email: Optional[EmailStr]
#     course: Optional[str]
#     gpa: Optional[float]

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "name": "Jane Doe",
#                 "email": "jdoe@example.com",
#                 "course": "Experiments, Science, and Fashion in Nanophotonics",
#                 "gpa": "3.0",
#             }
#         }
