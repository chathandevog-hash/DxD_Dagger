from database.mongo import db

COL = "thumbs"

async def set_thumb(user_id: int, file_id: str):
    await db[COL].update_one(
        {"user_id": user_id},
        {"$set": {"file_id": file_id}},
        upsert=True
    )

async def get_thumb(user_id: int):
    return await db[COL].find_one({"user_id": user_id})

async def delete_thumb(user_id: int):
    await db[COL].delete_one({"user_id": user_id})
