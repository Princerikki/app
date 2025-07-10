from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    match_id: str
    sender_id: str
    receiver_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

class MessageCreate(BaseModel):
    match_id: str
    receiver_id: str
    content: str

class MessageResponse(BaseModel):
    id: str
    match_id: str
    sender_id: str
    receiver_id: str
    content: str
    created_at: datetime
    is_read: bool
    is_current_user: bool = False