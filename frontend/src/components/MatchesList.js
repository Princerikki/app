import React from 'react';
import { Card, CardContent } from './ui/card';
import { Avatar, AvatarImage, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';
import { MessageCircle, Heart } from 'lucide-react';
import { mockMatches } from '../data/mock';

const MatchesList = ({ onChatClick }) => {
  if (mockMatches.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8">
        <div className="text-6xl mb-4">💔</div>
        <h2 className="text-2xl font-bold mb-2">No matches yet</h2>
        <p className="text-gray-600 mb-6">Start swiping to find your perfect match!</p>
        <div className="flex items-center space-x-2 text-pink-600">
          <Heart className="w-5 h-5" />
          <span className="font-medium">Keep swiping!</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold mb-2">Your Matches</h2>
        <p className="text-gray-600">
          {mockMatches.length} {mockMatches.length === 1 ? 'match' : 'matches'} waiting for you!
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {mockMatches.slice(0, 4).map((match) => (
          <Card key={match.id} className="relative overflow-hidden group cursor-pointer hover:shadow-lg transition-all duration-300">
            <div className="aspect-square bg-gradient-to-br from-pink-100 to-red-100 relative">
              <img
                src={match.photo}
                alt={match.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors duration-300" />
              <div className="absolute bottom-2 left-2 text-white">
                <p className="font-semibold text-sm">{match.name}</p>
              </div>
              <div className="absolute top-2 right-2">
                <div className="w-3 h-3 bg-pink-500 rounded-full animate-pulse"></div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="space-y-3">
        <h3 className="text-lg font-semibold">Messages</h3>
        {mockMatches.map((match) => (
          <Card
            key={match.id}
            className="cursor-pointer hover:shadow-md transition-shadow duration-200"
            onClick={() => onChatClick(match.id)}
          >
            <CardContent className="p-4">
              <div className="flex items-center space-x-4">
                <Avatar className="w-14 h-14">
                  <AvatarImage src={match.photo} alt={match.name} />
                  <AvatarFallback>{match.name[0]}</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-lg">{match.name}</h4>
                    <div className="flex items-center space-x-2">
                      {match.unread && (
                        <Badge variant="secondary" className="bg-pink-500 text-white">
                          New
                        </Badge>
                      )}
                      <span className="text-sm text-gray-500">{match.timestamp}</span>
                    </div>
                  </div>
                  <p className="text-gray-600 truncate">{match.lastMessage}</p>
                </div>
                <MessageCircle className="w-5 h-5 text-gray-400" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default MatchesList;