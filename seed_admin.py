"""
Seed script to create an admin user in the database.
Run this once to set up your first admin account.

Usage:
    python seed_admin.py
"""
import asyncio
import bcrypt
from database import user_collection
from datetime import datetime, timezone

ADMIN_EMAIL = "admin@jetintel.com"
ADMIN_PASSWORD = "admin@123"    # Change this in production!
ADMIN_NAME = "JetIntel Admin"


async def seed_admin():
    # Check if admin already exists
    existing = await user_collection.find_one({"email": ADMIN_EMAIL})
    if existing:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
        return

    # Create unique index on email field (ensures no duplicate emails)
    await user_collection.create_index("email", unique=True)

    admin_user = {
        "email": ADMIN_EMAIL,
        "password": bcrypt.hashpw(ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "name": ADMIN_NAME,
        "role": "admin",
        "created_at": datetime.now(timezone.utc),
    }

    await user_collection.insert_one(admin_user)
    print(f"Admin user created successfully!")
    print(f"  Email:    {ADMIN_EMAIL}")
    print(f"  Password: {ADMIN_PASSWORD}")
    print(f"  Role:     admin")
    print(f"\n⚠️  Change the default password after first login!")


asyncio.run(seed_admin())
