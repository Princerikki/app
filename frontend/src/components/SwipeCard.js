import React, { useState, useRef } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Heart, X, MapPin, Briefcase, GraduationCap } from 'lucide-react';

const SwipeCard = ({ user, onSwipe, isTopCard = false }) => {
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const cardRef = useRef(null);
  const startPos = useRef({ x: 0, y: 0 });

  const handleMouseDown = (e) => {
    if (!isTopCard) return;
    setIsDragging(true);
    startPos.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e) => {
    if (!isDragging || !isTopCard) return;
    const deltaX = e.clientX - startPos.current.x;
    const deltaY = e.clientY - startPos.current.y;
    setDragOffset({ x: deltaX, y: deltaY });
  };

  const handleMouseUp = () => {
    if (!isDragging || !isTopCard) return;
    setIsDragging(false);
    
    const threshold = 100;
    if (Math.abs(dragOffset.x) > threshold) {
      const direction = dragOffset.x > 0 ? 'right' : 'left';
      onSwipe(user.id, direction);
    }
    
    setDragOffset({ x: 0, y: 0 });
  };

  const handlePhotoClick = (e) => {
    if (isDragging) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const isRightHalf = clickX > rect.width / 2;
    
    if (isRightHalf && currentPhotoIndex < user.photos.length - 1) {
      setCurrentPhotoIndex(currentPhotoIndex + 1);
    } else if (!isRightHalf && currentPhotoIndex > 0) {
      setCurrentPhotoIndex(currentPhotoIndex - 1);
    }
  };

  const rotation = dragOffset.x * 0.1;
  const opacity = 1 - Math.abs(dragOffset.x) / 300;

  return (
    <Card
      ref={cardRef}
      className={`relative w-full h-[600px] cursor-grab active:cursor-grabbing overflow-hidden ${
        isTopCard ? 'z-10' : 'z-0'
      } transition-all duration-300 ease-out`}
      style={{
        transform: `translateX(${dragOffset.x}px) translateY(${dragOffset.y}px) rotate(${rotation}deg)`,
        opacity: isTopCard ? opacity : 0.8,
        scale: isTopCard ? 1 : 0.95
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* Photo indicator dots */}
      <div className="absolute top-4 left-1/2 transform -translate-x-1/2 flex space-x-2 z-20">
        {user.photos.map((_, index) => (
          <div
            key={index}
            className={`w-2 h-2 rounded-full transition-all duration-300 ${
              index === currentPhotoIndex ? 'bg-white' : 'bg-white/50'
            }`}
          />
        ))}
      </div>

      {/* Swipe direction indicators */}
      <div className={`absolute inset-0 flex items-center justify-center transition-opacity duration-300 ${
        dragOffset.x > 50 ? 'opacity-100' : 'opacity-0'
      }`}>
        <div className="bg-green-500 text-white px-4 py-2 rounded-full flex items-center space-x-2 text-lg font-bold">
          <Heart className="w-6 h-6" />
          <span>LIKE</span>
        </div>
      </div>

      <div className={`absolute inset-0 flex items-center justify-center transition-opacity duration-300 ${
        dragOffset.x < -50 ? 'opacity-100' : 'opacity-0'
      }`}>
        <div className="bg-red-500 text-white px-4 py-2 rounded-full flex items-center space-x-2 text-lg font-bold">
          <X className="w-6 h-6" />
          <span>NOPE</span>
        </div>
      </div>

      {/* Photo */}
      <div
        className="w-full h-full bg-cover bg-center cursor-pointer"
        style={{ backgroundImage: `url(${user.photos[currentPhotoIndex]})` }}
        onClick={handlePhotoClick}
      />

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />

      {/* User info */}
      <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
        <div className="flex items-center space-x-2 mb-2">
          <h2 className="text-3xl font-bold">{user.name}</h2>
          <span className="text-2xl font-light">{user.age}</span>
        </div>
        
        <div className="flex items-center space-x-2 mb-3 text-sm opacity-90">
          <MapPin className="w-4 h-4" />
          <span>{user.distance} km away</span>
        </div>

        <p className="text-sm mb-3 opacity-90 line-clamp-2">{user.bio}</p>

        <div className="flex items-center space-x-4 text-xs opacity-80 mb-3">
          <div className="flex items-center space-x-1">
            <Briefcase className="w-4 h-4" />
            <span>{user.occupation}</span>
          </div>
          <div className="flex items-center space-x-1">
            <GraduationCap className="w-4 h-4" />
            <span>{user.education}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {user.interests.slice(0, 3).map((interest, index) => (
            <Badge key={index} variant="secondary" className="text-xs">
              {interest}
            </Badge>
          ))}
        </div>
      </div>
    </Card>
  );
};

export default SwipeCard;