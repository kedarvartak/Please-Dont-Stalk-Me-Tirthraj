from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from .schemas.auth import UserCreate, Token, VerificationCode
from .services.auth_service import AuthService
from .database import get_database, connect_to_mongodb, close_mongodb_connection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr

# This line is crucial - it creates the FastAPI application instance
app = FastAPI()  # Make sure this line exists!

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # SvelteKit dev server
        "http://localhost:4173",  # SvelteKit preview
        "https://your-production-domain.com"  # prodction cha domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongodb()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()

@app.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await AuthService.register_user(db, user_data)
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await AuthService.authenticate_user(
        db,
        form_data.username,  # username field contains email
        form_data.password
    )

@app.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    return {"email": token}

@app.post("/verify-email")
async def verify_email(
    verification_data: VerificationCode,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    return await AuthService.verify_email(db, verification_data)

@app.post("/resend-verification")
async def resend_verification(
    email: EmailStr,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Implementation similar to register but only for resending code
    return await AuthService.resend_verification_code(db, email)
