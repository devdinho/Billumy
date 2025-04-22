from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://billumy-mongo:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["billumy"]
chat_collection = db["chats"]
