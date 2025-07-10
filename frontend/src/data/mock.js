// Mock data for the Tinder clone
export const mockUsers = [
  {
    id: 1,
    name: "Emma",
    age: 25,
    bio: "Adventure seeker 🏔️ Coffee enthusiast ☕ Dog lover 🐕 Always up for spontaneous road trips!",
    photos: [
      "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1521146764736-56c929d59c83?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&h=600&fit=crop"
    ],
    distance: 2,
    occupation: "Photographer",
    education: "Art Institute",
    interests: ["Photography", "Hiking", "Coffee", "Travel"]
  },
  {
    id: 2,
    name: "Alex",
    age: 28,
    bio: "Musician by night, developer by day 🎸 Love live music and good conversations 🎵",
    photos: [
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=600&fit=crop"
    ],
    distance: 5,
    occupation: "Software Developer",
    education: "Tech University",
    interests: ["Music", "Guitar", "Coding", "Concerts"]
  },
  {
    id: 3,
    name: "Sofia",
    age: 23,
    bio: "Yoga instructor & wellness coach 🧘‍♀️ Seeking genuine connections and positive vibes ✨",
    photos: [
      "https://images.unsplash.com/photo-1494790108755-2616c48f0054?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1506863530036-1efeddceb993?w=400&h=600&fit=crop"
    ],
    distance: 1,
    occupation: "Yoga Instructor",
    education: "Wellness Institute",
    interests: ["Yoga", "Meditation", "Healthy Living", "Nature"]
  },
  {
    id: 4,
    name: "Marcus",
    age: 30,
    bio: "Chef & food enthusiast 👨‍🍳 Love trying new cuisines and cooking for others 🍳",
    photos: [
      "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&h=600&fit=crop"
    ],
    distance: 8,
    occupation: "Chef",
    education: "Culinary School",
    interests: ["Cooking", "Food", "Wine", "Restaurants"]
  },
  {
    id: 5,
    name: "Luna",
    age: 26,
    bio: "Artist & creative soul 🎨 Painting my way through life one canvas at a time 🖌️",
    photos: [
      "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=400&h=600&fit=crop",
      "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=600&fit=crop"
    ],
    distance: 3,
    occupation: "Artist",
    education: "Fine Arts College",
    interests: ["Painting", "Art", "Museums", "Design"]
  }
];

export const mockCurrentUser = {
  id: "current-user",
  name: "You",
  age: 27,
  bio: "Looking for genuine connections and fun adventures! 🌟",
  photos: [
    "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400&h=600&fit=crop"
  ],
  occupation: "Marketing Manager",
  education: "Business School",
  interests: ["Travel", "Movies", "Fitness", "Food"],
  preferences: {
    minAge: 21,
    maxAge: 35,
    maxDistance: 25
  }
};

export const mockMatches = [
  {
    id: 1,
    name: "Emma",
    photo: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=600&fit=crop",
    lastMessage: "Hey! Thanks for the match! 😊",
    timestamp: "2h ago",
    unread: true
  },
  {
    id: 2,
    name: "Sofia",
    photo: "https://images.unsplash.com/photo-1494790108755-2616c48f0054?w=400&h=600&fit=crop",
    lastMessage: "That coffee place looks amazing!",
    timestamp: "1d ago",
    unread: false
  },
  {
    id: 3,
    name: "Luna",
    photo: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=600&fit=crop",
    lastMessage: "I love your art collection!",
    timestamp: "3d ago",
    unread: false
  }
];

export const mockMessages = {
  1: [
    {
      id: 1,
      senderId: 1,
      text: "Hey! Thanks for the match! 😊",
      timestamp: "2h ago",
      isCurrentUser: false
    },
    {
      id: 2,
      senderId: "current-user",
      text: "Hi Emma! Love your photography work!",
      timestamp: "1h ago",
      isCurrentUser: true
    },
    {
      id: 3,
      senderId: 1,
      text: "Thank you! I saw you're into hiking too. Know any good trails around here?",
      timestamp: "45m ago",
      isCurrentUser: false
    }
  ],
  2: [
    {
      id: 1,
      senderId: 2,
      text: "That coffee place looks amazing!",
      timestamp: "1d ago",
      isCurrentUser: false
    },
    {
      id: 2,
      senderId: "current-user",
      text: "Right? We should check it out sometime!",
      timestamp: "1d ago",
      isCurrentUser: true
    }
  ]
};

// Mock functions for localStorage simulation
export const mockLocalStorage = {
  likedUsers: new Set(),
  dislikedUsers: new Set(),
  matches: new Set(),
  
  like: (userId) => {
    mockLocalStorage.likedUsers.add(userId);
    // Simulate random matching (30% chance)
    if (Math.random() < 0.3) {
      mockLocalStorage.matches.add(userId);
      return true; // It's a match!
    }
    return false;
  },
  
  dislike: (userId) => {
    mockLocalStorage.dislikedUsers.add(userId);
  },
  
  isLiked: (userId) => mockLocalStorage.likedUsers.has(userId),
  isDisliked: (userId) => mockLocalStorage.dislikedUsers.has(userId),
  isMatched: (userId) => mockLocalStorage.matches.has(userId)
};