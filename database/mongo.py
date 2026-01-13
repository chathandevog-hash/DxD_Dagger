from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DB_NAME

mongo = None
db = None

async def init_db():
    global mongo, db
    mongo = AsyncIOMotorClient(MONGO_URL)
    db = mongo[DB_NAME]
    print("✅ MongoDB connected")
