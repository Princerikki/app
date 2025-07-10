from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.user import UserUpdate, UserResponse, UserProfile
from services.database import DatabaseService
from routes.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    # Prepare update data
    update_fields = {}
    if update_data.name is not None:
        update_fields["name"] = update_data.name
    if update_data.age is not None:
        update_fields["age"] = update_data.age
    if update_data.bio is not None:
        update_fields["bio"] = update_data.bio
    if update_data.occupation is not None:
        update_fields["occupation"] = update_data.occupation
    if update_data.education is not None:
        update_fields["education"] = update_data.education
    if update_data.interests is not None:
        update_fields["interests"] = update_data.interests
    if update_data.preferences is not None:
        update_fields["preferences"] = update_data.preferences.dict()
    
    update_fields["updated_at"] = datetime.utcnow()
    
    # Update user
    success = await DatabaseService.update_user(current_user["id"], update_fields)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update profile")
    
    # Get updated user
    updated_user = await DatabaseService.get_user_by_id(current_user["id"])
    
    return UserResponse(
        id=updated_user["id"],
        email=updated_user["email"],
        name=updated_user["name"],
        age=updated_user["age"],
        bio=updated_user["bio"],
        photos=updated_user["photos"],
        occupation=updated_user["occupation"],
        education=updated_user["education"],
        interests=updated_user["interests"],
        preferences=updated_user["preferences"],
        created_at=updated_user["created_at"]
    )

@router.get("/discover", response_model=List[UserProfile])
async def discover_users(current_user: dict = Depends(get_current_user)):
    """Get potential matches for the current user"""
    # Get users the current user has already swiped on
    swiped_user_ids = await DatabaseService.get_user_swipes(current_user["id"])
    
    # Get potential matches
    potential_matches = await DatabaseService.get_potential_matches(
        current_user["id"],
        current_user["preferences"],
        swiped_user_ids
    )
    
    # Convert to UserProfile format
    profiles = []
    for user in potential_matches:
        profile = UserProfile(
            id=user["id"],
            name=user["name"],
            age=user["age"],
            bio=user["bio"],
            photos=user["photos"],
            occupation=user["occupation"],
            education=user["education"],
            interests=user["interests"],
            distance=2  # Mock distance for now
        )
        profiles.append(profile)
    
    return profiles

@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific user's profile"""
    user = await DatabaseService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfile(
        id=user["id"],
        name=user["name"],
        age=user["age"],
        bio=user["bio"],
        photos=user["photos"],
        occupation=user["occupation"],
        education=user["education"],
        interests=user["interests"],
        distance=2  # Mock distance for now
    )