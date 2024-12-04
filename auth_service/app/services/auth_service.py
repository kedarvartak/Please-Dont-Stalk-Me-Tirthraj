from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.user import UserModel
from ..schemas.auth import UserCreate, VerificationCode
from ..utils.security import get_password_hash, verify_password, create_access_token
from datetime import datetime, timedelta
from ..services.email_service import EmailService
from bson.objectid import ObjectId

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
        
        # Generate verification code
        verification_code = EmailService.generate_verification_code()
        expires = datetime.utcnow() + timedelta(minutes=10)

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "_id": ObjectId(),
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "is_verified": False,
            "verification_code": verification_code,
            "verification_code_expires": expires,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        # Send verification email
        email_sent = await EmailService.send_verification_email(
            user_data.email, 
            verification_code
        )

        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send verification email")

        # Insert into MongoDB
        await db.users.insert_one(user_dict)
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

    @staticmethod
    async def verify_email(db: AsyncIOMotorDatabase, verification_data: VerificationCode):
        user = await db.users.find_one({"email": verification_data.email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user["is_verified"]:
            raise HTTPException(status_code=400, detail="Email already verified")

        if user["verification_code"] != verification_data.code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        if datetime.utcnow() > user["verification_code_expires"]:
            raise HTTPException(status_code=400, detail="Verification code expired")

        # Update user as verified
        await db.users.update_one(
            {"email": verification_data.email},
            {"$set": {"is_verified": True, "verification_code": None}}
        )

        return {"message": "Email verified successfully"}