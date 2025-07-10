from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.match import MatchResponse
from services.database import DatabaseService
from routes.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[MatchResponse])
async def get_matches(current_user: dict = Depends(get_current_user)):
    """Get all matches for the current user"""
    # Get matches from database
    matches = await DatabaseService.get_user_matches(current_user["id"])
    
    # Convert to response format
    match_responses = []
    for match in matches:
        # Determine the other user ID
        other_user_id = match["user2_id"] if match["user1_id"] == current_user["id"] else match["user1_id"]
        
        # Get other user's profile
        other_user = await DatabaseService.get_user_by_id(other_user_id)
        if other_user:
            # Get latest message for this match
            messages = await DatabaseService.get_match_messages(match["id"])
            last_message = messages[-1] if messages else None
            
            match_response = MatchResponse(
                id=match["id"],
                user_id=other_user["id"],
                user_name=other_user["name"],
                user_photo=other_user["photos"][0] if other_user["photos"] else None,
                last_message=last_message["content"] if last_message else None,
                last_message_at=last_message["created_at"] if last_message else None,
                created_at=match["created_at"],
                unread_count=0  # TODO: Implement unread count
            )
            match_responses.append(match_response)
    
    # Sort by last message time (most recent first)
    match_responses.sort(key=lambda x: x.last_message_at or x.created_at, reverse=True)
    
    return match_responses