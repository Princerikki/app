import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Heart, X, RotateCcw, Zap } from 'lucide-react';
import SwipeCard from './SwipeCard';
import { mockUsers, mockLocalStorage } from '../data/mock';
import { useToast } from '../hooks/use-toast';

const SwipeInterface = () => {
  const [users, setUsers] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    // Filter out already swiped users
    const availableUsers = mockUsers.filter(user => 
      !mockLocalStorage.isLiked(user.id) && !mockLocalStorage.isDisliked(user.id)
    );
    setUsers(availableUsers);
  }, []);

  const handleSwipe = (userId, direction) => {
    if (isAnimating) return;
    
    setIsAnimating(true);
    
    setTimeout(() => {
      if (direction === 'right') {
        const isMatch = mockLocalStorage.like(userId);
        if (isMatch) {
          toast({
            title: "It's a Match! 🎉",
            description: "You both liked each other!",
            duration: 3000,
          });
        }
      } else {
        mockLocalStorage.dislike(userId);
      }
      
      setCurrentIndex(prev => prev + 1);
      setIsAnimating(false);
    }, 300);
  };

  const handleLike = () => {
    if (currentIndex < users.length) {
      handleSwipe(users[currentIndex].id, 'right');
    }
  };

  const handleDislike = () => {
    if (currentIndex < users.length) {
      handleSwipe(users[currentIndex].id, 'left');
    }
  };

  const handleSuperLike = () => {
    if (currentIndex < users.length) {
      toast({
        title: "Super Like sent! ⭐",
        description: "They'll know you're really interested!",
        duration: 2000,
      });
      handleSwipe(users[currentIndex].id, 'right');
    }
  };

  if (currentIndex >= users.length) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-2xl font-bold mb-2">You're all caught up!</h2>
        <p className="text-gray-600 mb-6">No more profiles to show right now.</p>
        <Button 
          onClick={() => window.location.reload()} 
          className="bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600"
        >
          <RotateCcw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Cards Stack */}
      <div className="flex-1 relative p-4">
        <div className="relative w-full max-w-sm mx-auto h-full">
          {users.slice(currentIndex, currentIndex + 3).map((user, index) => (
            <div
              key={user.id}
              className="absolute inset-0"
              style={{
                zIndex: 3 - index,
                transform: `scale(${1 - index * 0.05}) translateY(${index * 10}px)`,
              }}
            >
              <SwipeCard
                user={user}
                onSwipe={handleSwipe}
                isTopCard={index === 0}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center items-center space-x-6 p-6 bg-white border-t">
        <Button
          variant="outline"
          size="lg"
          className="w-14 h-14 rounded-full border-2 border-red-500 text-red-500 hover:bg-red-50 hover:border-red-600 hover:text-red-600 transition-all duration-200"
          onClick={handleDislike}
          disabled={isAnimating}
        >
          <X className="w-6 h-6" />
        </Button>
        
        <Button
          variant="outline"
          size="lg"
          className="w-12 h-12 rounded-full border-2 border-blue-500 text-blue-500 hover:bg-blue-50 hover:border-blue-600 hover:text-blue-600 transition-all duration-200"
          onClick={handleSuperLike}
          disabled={isAnimating}
        >
          <Zap className="w-5 h-5" />
        </Button>
        
        <Button
          variant="outline"
          size="lg"
          className="w-14 h-14 rounded-full border-2 border-green-500 text-green-500 hover:bg-green-50 hover:border-green-600 hover:text-green-600 transition-all duration-200"
          onClick={handleLike}
          disabled={isAnimating}
        >
          <Heart className="w-6 h-6" />
        </Button>
      </div>
    </div>
  );
};

export default SwipeInterface;