from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import certifi
import ssl

class Database:
    client: AsyncIOMotorClient = None
    
async def get_database():
    """Return database instance"""
    return Database.client[settings.DB_NAME]

async def connect_to_mongodb():
    """Create database connection."""
    try:
        Database.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        # Verify the connection
        await Database.client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongodb_connection():
    """Close database connection."""
    if Database.client:
        Database.client.close()
        print("MongoDB connection closed!") 