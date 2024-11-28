from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.user import UserModel
from ..schemas.auth import UserCreate
from ..utils.security import get_password_hash, verify_password, create_access_token

class AuthService:
    @staticmethod
    async def register_user(db: AsyncIOMotorDatabase, user_data: UserCreate) -> UserModel:
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "is_active": True
        }
        
        # Insert into MongoDB
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return UserModel(**user_dict)

    @staticmethod
    async def authenticate_user(db: AsyncIOMotorDatabase, email: str, password: str) -> dict:
        # Find user in MongoDB
        user = await db.users.find_one({"email": email})
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}