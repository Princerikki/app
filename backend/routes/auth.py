from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models.user import UserCreate, UserLogin, UserResponse, User
from services.auth import hash_password, verify_password, create_access_token, verify_token
from services.database import DatabaseService
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = await DatabaseService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate):
    """Register a new user"""
    # Check if user already exists
    existing_user = await DatabaseService.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user object
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name,
        age=user_data.age,
        bio=user_data.bio or "",
        occupation=user_data.occupation or "",
        education=user_data.education or "",
        photos=[],
        interests=[]
    )
    
    # Save to database
    created_user = await DatabaseService.create_user(user.dict())
    
    # Create access token
    access_token = create_access_token(data={"user_id": created_user["id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=created_user["id"],
            email=created_user["email"],
            name=created_user["name"],
            age=created_user["age"],
            bio=created_user["bio"],
            photos=created_user["photos"],
            occupation=created_user["occupation"],
            education=created_user["education"],
            interests=created_user["interests"],
            preferences=created_user["preferences"],
            created_at=created_user["created_at"]
        )
    }

@router.post("/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login user"""
    # Get user by email
    user = await DatabaseService.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token = create_access_token(data={"user_id": user["id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            age=user["age"],
            bio=user["bio"],
            photos=user["photos"],
            occupation=user["occupation"],
            education=user["education"],
            interests=user["interests"],
            preferences=user["preferences"],
            created_at=user["created_at"]
        )
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        age=current_user["age"],
        bio=current_user["bio"],
        photos=current_user["photos"],
        occupation=current_user["occupation"],
        education=current_user["education"],
        interests=current_user["interests"],
        preferences=current_user["preferences"],
        created_at=current_user["created_at"]
    )