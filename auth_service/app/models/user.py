from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            v = ObjectId(v)
        return v

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator: Any) -> dict[str, Any]:
        return {"type": "string"}
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = False
    verification_code: Optional[str] = None
    verification_code_expires: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
