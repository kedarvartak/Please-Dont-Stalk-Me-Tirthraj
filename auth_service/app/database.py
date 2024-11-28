from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    
async def get_database():
    """Return database instance"""
    return Database.client[settings.DB_NAME]

async def connect_to_mongodb():
    """Create database connection."""
    Database.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("Connected to MongoDB!")

async def close_mongodb_connection():
    """Close database connection."""
    if Database.client:
        Database.client.close()
        print("MongoDB connection closed!") 