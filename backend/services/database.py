from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any
import os

# Database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
users_collection = db.users
swipes_collection = db.swipes
matches_collection = db.matches
messages_collection = db.messages

class DatabaseService:
    @staticmethod
    async def create_user(user_data: dict) -> dict:
        """Create a new user"""
        result = await users_collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return user_data
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        user = await users_collection.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        """Get user by ID"""
        user = await users_collection.find_one({"id": user_id})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> bool:
        """Update user data"""
        result = await users_collection.update_one(
            {"id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    async def get_potential_matches(user_id: str, user_preferences: dict, swiped_user_ids: List[str]) -> List[dict]:
        """Get potential matches for a user"""
        query = {
            "id": {"$ne": user_id},
            "id": {"$nin": swiped_user_ids},
            "age": {
                "$gte": user_preferences.get("min_age", 18),
                "$lte": user_preferences.get("max_age", 35)
            },
            "is_active": True
        }
        
        users = await users_collection.find(query).limit(10).to_list(length=10)
        for user in users:
            user['_id'] = str(user['_id'])
        return users
    
    @staticmethod
    async def create_swipe(swipe_data: dict) -> dict:
        """Create a swipe record"""
        result = await swipes_collection.insert_one(swipe_data)
        swipe_data['_id'] = str(result.inserted_id)
        return swipe_data
    
    @staticmethod
    async def get_swipe(swiper_id: str, swiped_id: str) -> Optional[dict]:
        """Get existing swipe between two users"""
        swipe = await swipes_collection.find_one({
            "swiper_id": swiper_id,
            "swiped_id": swiped_id
        })
        if swipe:
            swipe['_id'] = str(swipe['_id'])
        return swipe
    
    @staticmethod
    async def get_user_swipes(user_id: str) -> List[str]:
        """Get all user IDs that a user has swiped on"""
        swipes = await swipes_collection.find({"swiper_id": user_id}).to_list(length=None)
        return [swipe['swiped_id'] for swipe in swipes]
    
    @staticmethod
    async def check_mutual_like(user1_id: str, user2_id: str) -> bool:
        """Check if both users liked each other"""
        swipe1 = await swipes_collection.find_one({
            "swiper_id": user1_id,
            "swiped_id": user2_id,
            "action": "like"
        })
        swipe2 = await swipes_collection.find_one({
            "swiper_id": user2_id,
            "swiped_id": user1_id,
            "action": "like"
        })
        return swipe1 is not None and swipe2 is not None
    
    @staticmethod
    async def create_match(match_data: dict) -> dict:
        """Create a match record"""
        result = await matches_collection.insert_one(match_data)
        match_data['_id'] = str(result.inserted_id)
        return match_data
    
    @staticmethod
    async def get_user_matches(user_id: str) -> List[dict]:
        """Get all matches for a user"""
        matches = await matches_collection.find({
            "$or": [
                {"user1_id": user_id},
                {"user2_id": user_id}
            ],
            "is_active": True
        }).to_list(length=None)
        
        for match in matches:
            match['_id'] = str(match['_id'])
        return matches
    
    @staticmethod
    async def create_message(message_data: dict) -> dict:
        """Create a message"""
        result = await messages_collection.insert_one(message_data)
        message_data['_id'] = str(result.inserted_id)
        return message_data
    
    @staticmethod
    async def get_match_messages(match_id: str) -> List[dict]:
        """Get all messages for a match"""
        messages = await messages_collection.find({
            "match_id": match_id
        }).sort("created_at", 1).to_list(length=None)
        
        for message in messages:
            message['_id'] = str(message['_id'])
        return messages
    
    @staticmethod
    async def update_match_last_message(match_id: str, last_message_at: Any) -> bool:
        """Update the last message time for a match"""
        result = await matches_collection.update_one(
            {"id": match_id},
            {"$set": {"last_message_at": last_message_at}}
        )
        return result.modified_count > 0