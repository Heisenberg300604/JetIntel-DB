from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["jet_database"]

jet_collection = db["jets"]
airport_collection = db["airports"]
user_collection = db["users"]