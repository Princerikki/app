from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class SwipeAction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    swiper_id: str  # User who performed the swipe
    swiped_id: str  # User who was swiped
    action: str  # "like", "dislike", "super_like"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SwipeCreate(BaseModel):
    swiped_id: str
    action: str  # "like", "dislike", "super_like"

class SwipeResponse(BaseModel):
    id: str
    swiped_id: str
    action: str
    created_at: datetime
    is_match: bool = False