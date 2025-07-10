#!/usr/bin/env python3
"""
Comprehensive Backend API Test Suite for Tinder Clone
Tests all authentication, user, swipe, match, and message endpoints
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://67f326a2-bf4d-4a60-97a7-ebdc378cdba3.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class TinderAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS.copy()
        self.user1_token = None
        self.user2_token = None
        self.user1_id = None
        self.user2_id = None
        self.match_id = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    auth_token: Optional[str] = None) -> tuple[bool, Dict]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
            
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}
                
            return response.status_code < 400, {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}
        except json.JSONDecodeError as e:
            return False, {"error": f"JSON decode error: {str(e)}"}
            
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        print("\n=== Testing Basic Connectivity ===")
        success, response = self.make_request("GET", "/")
        
        if success and response["status_code"] == 200:
            self.log_test("Basic API Connectivity", True, f"API responded: {response['data'].get('message', 'OK')}")
        else:
            self.log_test("Basic API Connectivity", False, f"Failed to connect: {response}")
            
    def test_auth_signup(self):
        """Test user signup functionality"""
        print("\n=== Testing Authentication - Signup ===")
        
        # Test User 1 Signup
        user1_data = {
            "email": "emma.watson@example.com",
            "password": "SecurePass123!",
            "name": "Emma Watson",
            "age": 28,
            "bio": "Actress and activist passionate about books and social causes",
            "occupation": "Actress",
            "education": "Brown University"
        }
        
        success, response = self.make_request("POST", "/auth/signup", user1_data)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if "access_token" in data and "user" in data:
                self.user1_token = data["access_token"]
                self.user1_id = data["user"]["id"]
                self.log_test("User 1 Signup", True, f"Created user: {data['user']['name']}")
            else:
                self.log_test("User 1 Signup", False, "Missing token or user data in response")
        else:
            self.log_test("User 1 Signup", False, f"Signup failed: {response}")
            
        # Test User 2 Signup
        user2_data = {
            "email": "ryan.gosling@example.com",
            "password": "SecurePass456!",
            "name": "Ryan Gosling",
            "age": 32,
            "bio": "Actor who loves jazz music and vintage cars",
            "occupation": "Actor",
            "education": "Gladstone Public School"
        }
        
        success, response = self.make_request("POST", "/auth/signup", user2_data)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if "access_token" in data and "user" in data:
                self.user2_token = data["access_token"]
                self.user2_id = data["user"]["id"]
                self.log_test("User 2 Signup", True, f"Created user: {data['user']['name']}")
            else:
                self.log_test("User 2 Signup", False, "Missing token or user data in response")
        else:
            self.log_test("User 2 Signup", False, f"Signup failed: {response}")
            
        # Test duplicate email signup
        success, response = self.make_request("POST", "/auth/signup", user1_data)
        if success and response["status_code"] == 400:
            self.log_test("Duplicate Email Signup Prevention", True, "Correctly rejected duplicate email")
        else:
            self.log_test("Duplicate Email Signup Prevention", False, "Should have rejected duplicate email")
            
    def test_auth_login(self):
        """Test user login functionality"""
        print("\n=== Testing Authentication - Login ===")
        
        # Test valid login
        login_data = {
            "email": "emma.watson@example.com",
            "password": "SecurePass123!"
        }
        
        success, response = self.make_request("POST", "/auth/login", login_data)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if "access_token" in data and "user" in data:
                self.log_test("Valid Login", True, f"Login successful for: {data['user']['name']}")
            else:
                self.log_test("Valid Login", False, "Missing token or user data in response")
        else:
            self.log_test("Valid Login", False, f"Login failed: {response}")
            
        # Test invalid login
        invalid_login_data = {
            "email": "emma.watson@example.com",
            "password": "WrongPassword"
        }
        
        success, response = self.make_request("POST", "/auth/login", invalid_login_data)
        if success and response["status_code"] == 401:
            self.log_test("Invalid Login Prevention", True, "Correctly rejected invalid credentials")
        else:
            self.log_test("Invalid Login Prevention", False, "Should have rejected invalid credentials")
            
    def test_auth_me(self):
        """Test get current user profile"""
        print("\n=== Testing Authentication - Get Me ===")
        
        if not self.user1_token:
            self.log_test("Get Current User Profile", False, "No auth token available")
            return
            
        success, response = self.make_request("GET", "/auth/me", auth_token=self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if "id" in data and "email" in data and "name" in data:
                self.log_test("Get Current User Profile", True, f"Retrieved profile for: {data['name']}")
            else:
                self.log_test("Get Current User Profile", False, "Missing required user fields")
        else:
            self.log_test("Get Current User Profile", False, f"Failed to get profile: {response}")
            
        # Test without auth token
        success, response = self.make_request("GET", "/auth/me")
        if success and response["status_code"] == 401:
            self.log_test("Unauthorized Access Prevention", True, "Correctly rejected request without token")
        else:
            self.log_test("Unauthorized Access Prevention", False, "Should have rejected request without token")
            
    def test_users_profile_update(self):
        """Test user profile update"""
        print("\n=== Testing Users - Profile Update ===")
        
        if not self.user1_token:
            self.log_test("Profile Update", False, "No auth token available")
            return
            
        update_data = {
            "bio": "Updated bio: Actress, activist, and book lover exploring new adventures",
            "interests": ["reading", "activism", "movies", "travel"],
            "preferences": {
                "min_age": 25,
                "max_age": 40,
                "max_distance": 30
            }
        }
        
        success, response = self.make_request("PUT", "/users/profile", update_data, self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if data.get("bio") == update_data["bio"]:
                self.log_test("Profile Update", True, "Profile updated successfully")
            else:
                self.log_test("Profile Update", False, "Profile data not updated correctly")
        else:
            self.log_test("Profile Update", False, f"Profile update failed: {response}")
            
    def test_users_discover(self):
        """Test user discovery"""
        print("\n=== Testing Users - Discover ===")
        
        if not self.user1_token:
            self.log_test("User Discovery", False, "No auth token available")
            return
            
        success, response = self.make_request("GET", "/users/discover", auth_token=self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if isinstance(data, list):
                self.log_test("User Discovery", True, f"Found {len(data)} potential matches")
                # Check if user2 is in the discovery list
                user2_found = any(user.get("id") == self.user2_id for user in data)
                if user2_found:
                    self.log_test("User 2 in Discovery", True, "User 2 appears in User 1's discovery")
                else:
                    self.log_test("User 2 in Discovery", False, "User 2 not found in User 1's discovery")
            else:
                self.log_test("User Discovery", False, "Response is not a list")
        else:
            self.log_test("User Discovery", False, f"Discovery failed: {response}")
            
    def test_swipes_functionality(self):
        """Test swiping functionality"""
        print("\n=== Testing Swipes - Swipe Functionality ===")
        
        if not self.user1_token or not self.user2_token or not self.user2_id or not self.user1_id:
            self.log_test("Swipe Functionality", False, "Missing required user data")
            return
            
        # User 1 likes User 2
        swipe_data = {
            "swiped_id": self.user2_id,
            "action": "like"
        }
        
        success, response = self.make_request("POST", "/swipes/swipe", swipe_data, self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if data.get("action") == "like" and data.get("swiped_id") == self.user2_id:
                is_match = data.get("is_match", False)
                self.log_test("User 1 Swipes User 2", True, f"Swipe successful, match: {is_match}")
            else:
                self.log_test("User 1 Swipes User 2", False, "Swipe data incorrect")
        else:
            self.log_test("User 1 Swipes User 2", False, f"Swipe failed: {response}")
            
        # User 2 likes User 1 (should create a match)
        swipe_data = {
            "swiped_id": self.user1_id,
            "action": "like"
        }
        
        success, response = self.make_request("POST", "/swipes/swipe", swipe_data, self.user2_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if data.get("action") == "like" and data.get("swiped_id") == self.user1_id:
                is_match = data.get("is_match", False)
                self.log_test("User 2 Swipes User 1", True, f"Swipe successful, match: {is_match}")
                if is_match:
                    self.log_test("Match Creation", True, "Match created successfully")
                else:
                    self.log_test("Match Creation", False, "Match should have been created")
            else:
                self.log_test("User 2 Swipes User 1", False, "Swipe data incorrect")
        else:
            self.log_test("User 2 Swipes User 1", False, f"Swipe failed: {response}")
            
        # Test duplicate swipe prevention
        success, response = self.make_request("POST", "/swipes/swipe", swipe_data, self.user2_token)
        if success and response["status_code"] == 400:
            self.log_test("Duplicate Swipe Prevention", True, "Correctly prevented duplicate swipe")
        else:
            self.log_test("Duplicate Swipe Prevention", False, "Should have prevented duplicate swipe")
            
    def test_matches_retrieval(self):
        """Test matches retrieval"""
        print("\n=== Testing Matches - Get Matches ===")
        
        if not self.user1_token:
            self.log_test("Get Matches", False, "No auth token available")
            return
            
        success, response = self.make_request("GET", "/matches/", auth_token=self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if isinstance(data, list):
                self.log_test("Get Matches", True, f"Retrieved {len(data)} matches")
                if len(data) > 0:
                    # Store match ID for message testing
                    self.match_id = data[0]["id"]
                    match_user_name = data[0].get("user_name", "Unknown")
                    self.log_test("Match Data Validation", True, f"Match with {match_user_name} found")
                else:
                    self.log_test("Match Data Validation", False, "No matches found (expected at least 1)")
            else:
                self.log_test("Get Matches", False, "Response is not a list")
        else:
            self.log_test("Get Matches", False, f"Get matches failed: {response}")
            
    def test_messages_functionality(self):
        """Test messaging functionality"""
        print("\n=== Testing Messages - Send and Retrieve ===")
        
        if not self.user1_token or not self.user2_token or not self.match_id or not self.user2_id:
            self.log_test("Message Functionality", False, "Missing required data for messaging")
            return
            
        # User 1 sends message to User 2
        message_data = {
            "match_id": self.match_id,
            "receiver_id": self.user2_id,
            "content": "Hey! Great to match with you! How's your day going?"
        }
        
        success, response = self.make_request("POST", "/messages/send", message_data, self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if data.get("content") == message_data["content"] and data.get("match_id") == self.match_id:
                self.log_test("Send Message (User 1 to User 2)", True, "Message sent successfully")
            else:
                self.log_test("Send Message (User 1 to User 2)", False, "Message data incorrect")
        else:
            self.log_test("Send Message (User 1 to User 2)", False, f"Send message failed: {response}")
            
        # User 2 sends reply to User 1
        reply_data = {
            "match_id": self.match_id,
            "receiver_id": self.user1_id,
            "content": "Hi there! My day is going great, thanks for asking! What about yours?"
        }
        
        success, response = self.make_request("POST", "/messages/send", reply_data, self.user2_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if data.get("content") == reply_data["content"]:
                self.log_test("Send Reply (User 2 to User 1)", True, "Reply sent successfully")
            else:
                self.log_test("Send Reply (User 2 to User 1)", False, "Reply data incorrect")
        else:
            self.log_test("Send Reply (User 2 to User 1)", False, f"Send reply failed: {response}")
            
        # Retrieve messages for the match
        success, response = self.make_request("GET", f"/messages/{self.match_id}", auth_token=self.user1_token)
        
        if success and response["status_code"] == 200:
            data = response["data"]
            if isinstance(data, list) and len(data) >= 2:
                self.log_test("Retrieve Messages", True, f"Retrieved {len(data)} messages")
                
                # Verify message order and content
                first_message = data[0]
                second_message = data[1]
                
                if (first_message.get("content") == message_data["content"] and 
                    second_message.get("content") == reply_data["content"]):
                    self.log_test("Message Order and Content", True, "Messages in correct order with correct content")
                else:
                    self.log_test("Message Order and Content", False, "Messages not in expected order or content")
            else:
                self.log_test("Retrieve Messages", False, f"Expected at least 2 messages, got {len(data) if isinstance(data, list) else 0}")
        else:
            self.log_test("Retrieve Messages", False, f"Retrieve messages failed: {response}")
            
    def test_complete_user_flow(self):
        """Test the complete user flow as described in requirements"""
        print("\n=== Testing Complete User Flow ===")
        
        # This is a summary test that validates the entire flow worked
        flow_success = (
            self.user1_token is not None and
            self.user2_token is not None and
            self.user1_id is not None and
            self.user2_id is not None and
            self.match_id is not None
        )
        
        if flow_success:
            self.log_test("Complete User Flow", True, "All components of user flow completed successfully")
        else:
            missing_components = []
            if not self.user1_token: missing_components.append("User 1 token")
            if not self.user2_token: missing_components.append("User 2 token")
            if not self.user1_id: missing_components.append("User 1 ID")
            if not self.user2_id: missing_components.append("User 2 ID")
            if not self.match_id: missing_components.append("Match ID")
            
            self.log_test("Complete User Flow", False, f"Missing: {', '.join(missing_components)}")
            
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Tinder Clone Backend API Tests")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run tests in logical order
        self.test_basic_connectivity()
        self.test_auth_signup()
        self.test_auth_login()
        self.test_auth_me()
        self.test_users_profile_update()
        self.test_users_discover()
        self.test_swipes_functionality()
        self.test_matches_retrieval()
        self.test_messages_functionality()
        self.test_complete_user_flow()
        
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['test']}: {result['details']}")
                    
        print("\n" + "=" * 60)
        
        # Return overall success
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = TinderAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed! Backend API is working correctly.")
        exit(0)
    else:
        print("⚠️  Some tests failed. Check the details above.")
        exit(1)

if __name__ == "__main__":
    main()