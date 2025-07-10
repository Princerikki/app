from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Match(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user1_id: str
    user2_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
    is_active: bool = True

class MatchResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    user_photo: Optional[str] = None
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    created_at: datetime
    unread_count: int = 0