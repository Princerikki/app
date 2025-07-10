from fastapi import APIRouter, HTTPException, Depends
from models.swipe import SwipeCreate, SwipeResponse, SwipeAction
from models.match import Match
from services.database import DatabaseService
from routes.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/swipe", response_model=SwipeResponse)
async def swipe_user(
    swipe_data: SwipeCreate,
    current_user: dict = Depends(get_current_user)
):
    """Swipe on a user (like, dislike, or super_like)"""
    # Check if user exists
    target_user = await DatabaseService.get_user_by_id(swipe_data.swiped_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user already swiped on this person
    existing_swipe = await DatabaseService.get_swipe(
        current_user["id"], 
        swipe_data.swiped_id
    )
    if existing_swipe:
        raise HTTPException(status_code=400, detail="Already swiped on this user")
    
    # Create swipe record
    swipe = SwipeAction(
        swiper_id=current_user["id"],
        swiped_id=swipe_data.swiped_id,
        action=swipe_data.action
    )
    
    created_swipe = await DatabaseService.create_swipe(swipe.dict())
    
    # Check for mutual like (match)
    is_match = False
    if swipe_data.action == "like":
        is_match = await DatabaseService.check_mutual_like(
            current_user["id"],
            swipe_data.swiped_id
        )
        
        # Create match if mutual like
        if is_match:
            match = Match(
                user1_id=current_user["id"],
                user2_id=swipe_data.swiped_id
            )
            await DatabaseService.create_match(match.dict())
    
    return SwipeResponse(
        id=created_swipe["id"],
        swiped_id=created_swipe["swiped_id"],
        action=created_swipe["action"],
        created_at=created_swipe["created_at"],
        is_match=is_match
    )