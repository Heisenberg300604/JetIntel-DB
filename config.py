import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URL = os.getenv("MONGO_URL")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "jetintel-super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
