from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class UserPreferences(BaseModel):
    min_age: int = Field(default=18, ge=18, le=100)
    max_age: int = Field(default=35, ge=18, le=100)
    max_distance: int = Field(default=25, ge=1, le=100)

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password_hash: str
    name: str
    age: int = Field(ge=18, le=100)
    bio: Optional[str] = ""
    photos: List[str] = []
    occupation: Optional[str] = ""
    education: Optional[str] = ""
    interests: List[str] = []
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    location: Optional[dict] = None  # {"lat": float, "lng": float}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    age: int = Field(ge=18, le=100)
    bio: Optional[str] = ""
    occupation: Optional[str] = ""
    education: Optional[str] = ""

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=100)
    bio: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    interests: Optional[List[str]] = None
    preferences: Optional[UserPreferences] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    age: int
    bio: str
    photos: List[str]
    occupation: str
    education: str
    interests: List[str]
    preferences: UserPreferences
    created_at: datetime

class UserProfile(BaseModel):
    id: str
    name: str
    age: int
    bio: str
    photos: List[str]
    occupation: str
    education: str
    interests: List[str]
    distance: Optional[int] = None