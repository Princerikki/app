import React from 'react';
import { Button } from './ui/button';
import { Heart, MessageCircle, User, LogOut, Flame } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navigation = ({ currentView, onViewChange }) => {
  const { logout } = useAuth();

  const navItems = [
    { id: 'discover', icon: Flame, label: 'Discover' },
    { id: 'matches', icon: Heart, label: 'Matches' },
    { id: 'profile', icon: User, label: 'Profile' },
  ];

  return (
    <div className="bg-white border-t border-gray-200 px-4 py-2">
      <div className="flex justify-around items-center max-w-sm mx-auto">
        {navItems.map(({ id, icon: Icon, label }) => (
          <Button
            key={id}
            variant="ghost"
            className={`flex flex-col items-center space-y-1 p-2 h-auto ${
              currentView === id
                ? 'text-pink-600 bg-pink-50'
                : 'text-gray-600 hover:text-pink-600 hover:bg-pink-50'
            }`}
            onClick={() => onViewChange(id)}
          >
            <Icon className="w-6 h-6" />
            <span className="text-xs font-medium">{label}</span>
          </Button>
        ))}
        <Button
          variant="ghost"
          className="flex flex-col items-center space-y-1 p-2 h-auto text-gray-600 hover:text-red-600 hover:bg-red-50"
          onClick={logout}
        >
          <LogOut className="w-6 h-6" />
          <span className="text-xs font-medium">Logout</span>
        </Button>
      </div>
    </div>
  );
};

export default Navigation;