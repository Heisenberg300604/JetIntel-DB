from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserRegister, UserLogin, UserResponse, TokenResponse
from database import user_collection
from middleware.auth import get_current_user
import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user account (default role: 'user').
    """
    # Check if email already exists
    existing = await user_collection.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash the password and store
    hashed_password = hash_password(user_data.password)
    new_user = {
        "email": user_data.email,
        "password": hashed_password,
        "name": user_data.name,
        "role": "user",  # default role
        "created_at": datetime.now(timezone.utc),
    }

    result = await user_collection.insert_one(new_user)
    user_id = str(result.inserted_id)

    # Generate JWT
    token = create_access_token({"sub": user_id, "role": "user"})

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=new_user["email"],
            name=new_user["name"],
            role=new_user["role"],
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Login with email and password. Returns JWT access token.
    """
    user = await user_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_id = str(user["_id"])
    token = create_access_token({"sub": user_id, "role": user["role"]})

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user["email"],
            name=user["name"],
            role=user["role"],
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current logged-in user info. Requires a valid JWT token.
    """
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        name=current_user["name"],
        role=current_user["role"],
    )
