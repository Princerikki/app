from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any

# Database will be initialized by server.py
client = None
db = None

def init_database(mongo_url: str, db_name: str):
    """Initialize database connection"""
    global client, db
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

# Collections
def get_users_collection():
    return db.users

def get_swipes_collection():
    return db.swipes

def get_matches_collection():
    return db.matches

def get_messages_collection():
    return db.messages

class DatabaseService:
    @staticmethod
    async def create_user(user_data: dict) -> dict:
        """Create a new user"""
        result = await get_users_collection().insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return user_data
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        user = await get_users_collection().find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        """Get user by ID"""
        user = await get_users_collection().find_one({"id": user_id})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> bool:
        """Update user data"""
        result = await get_users_collection().update_one(
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
        
        users = await get_users_collection().find(query).limit(10).to_list(length=10)
        for user in users:
            user['_id'] = str(user['_id'])
        return users
    
    @staticmethod
    async def create_swipe(swipe_data: dict) -> dict:
        """Create a swipe record"""
        result = await get_swipes_collection().insert_one(swipe_data)
        swipe_data['_id'] = str(result.inserted_id)
        return swipe_data
    
    @staticmethod
    async def get_swipe(swiper_id: str, swiped_id: str) -> Optional[dict]:
        """Get existing swipe between two users"""
        swipe = await get_swipes_collection().find_one({
            "swiper_id": swiper_id,
            "swiped_id": swiped_id
        })
        if swipe:
            swipe['_id'] = str(swipe['_id'])
        return swipe
    
    @staticmethod
    async def get_user_swipes(user_id: str) -> List[str]:
        """Get all user IDs that a user has swiped on"""
        swipes = await get_swipes_collection().find({"swiper_id": user_id}).to_list(length=None)
        return [swipe['swiped_id'] for swipe in swipes]
    
    @staticmethod
    async def check_mutual_like(user1_id: str, user2_id: str) -> bool:
        """Check if both users liked each other"""
        swipe1 = await get_swipes_collection().find_one({
            "swiper_id": user1_id,
            "swiped_id": user2_id,
            "action": "like"
        })
        swipe2 = await get_swipes_collection().find_one({
            "swiper_id": user2_id,
            "swiped_id": user1_id,
            "action": "like"
        })
        return swipe1 is not None and swipe2 is not None
    
    @staticmethod
    async def create_match(match_data: dict) -> dict:
        """Create a match record"""
        result = await get_matches_collection().insert_one(match_data)
        match_data['_id'] = str(result.inserted_id)
        return match_data
    
    @staticmethod
    async def get_user_matches(user_id: str) -> List[dict]:
        """Get all matches for a user"""
        matches = await get_matches_collection().find({
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
        result = await get_messages_collection().insert_one(message_data)
        message_data['_id'] = str(result.inserted_id)
        return message_data
    
    @staticmethod
    async def get_match_messages(match_id: str) -> List[dict]:
        """Get all messages for a match"""
        messages = await get_messages_collection().find({
            "match_id": match_id
        }).sort("created_at", 1).to_list(length=None)
        
        for message in messages:
            message['_id'] = str(message['_id'])
        return messages
    
    @staticmethod
    async def update_match_last_message(match_id: str, last_message_at: Any) -> bool:
        """Update the last message time for a match"""
        result = await get_matches_collection().update_one(
            {"id": match_id},
            {"$set": {"last_message_at": last_message_at}}
        )
        return result.modified_count > 0