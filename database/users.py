from database.mongo import db

COL = "users"

async def add_user(user_id: int):
    await db[COL].update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id}},
        upsert=True
    )
