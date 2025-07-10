from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.message import MessageCreate, MessageResponse, Message
from services.database import DatabaseService
from routes.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/send", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user)
):
    """Send a message to a matched user"""
    # Verify that the match exists and current user is part of it
    matches = await DatabaseService.get_user_matches(current_user["id"])
    match_exists = any(match["id"] == message_data.match_id for match in matches)
    
    if not match_exists:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Create message
    message = Message(
        match_id=message_data.match_id,
        sender_id=current_user["id"],
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )
    
    created_message = await DatabaseService.create_message(message.dict())
    
    # Update match's last message time
    await DatabaseService.update_match_last_message(
        message_data.match_id,
        created_message["created_at"]
    )
    
    return MessageResponse(
        id=created_message["id"],
        match_id=created_message["match_id"],
        sender_id=created_message["sender_id"],
        receiver_id=created_message["receiver_id"],
        content=created_message["content"],
        created_at=created_message["created_at"],
        is_read=created_message["is_read"],
        is_current_user=True
    )

@router.get("/{match_id}", response_model=List[MessageResponse])
async def get_messages(
    match_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all messages for a specific match"""
    # Verify that the match exists and current user is part of it
    matches = await DatabaseService.get_user_matches(current_user["id"])
    match_exists = any(match["id"] == match_id for match in matches)
    
    if not match_exists:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Get messages
    messages = await DatabaseService.get_match_messages(match_id)
    
    # Convert to response format
    message_responses = []
    for message in messages:
        message_response = MessageResponse(
            id=message["id"],
            match_id=message["match_id"],
            sender_id=message["sender_id"],
            receiver_id=message["receiver_id"],
            content=message["content"],
            created_at=message["created_at"],
            is_read=message["is_read"],
            is_current_user=message["sender_id"] == current_user["id"]
        )
        message_responses.append(message_response)
    
    return message_responses