import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Toaster } from './components/ui/toaster';
import AuthPages from './components/AuthPages';
import SwipeInterface from './components/SwipeInterface';
import MatchesList from './components/MatchesList';
import ChatInterface from './components/ChatInterface';
import ProfilePage from './components/ProfilePage';
import Navigation from './components/Navigation';

const MainApp = () => {
  const { user, loading } = useAuth();
  const [currentView, setCurrentView] = useState('discover');
  const [selectedChatId, setSelectedChatId] = useState(null);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-400 via-red-400 to-yellow-400 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <AuthPages />;
  }

  const handleChatClick = (matchId) => {
    setSelectedChatId(matchId);
    setCurrentView('chat');
  };

  const handleBackToMatches = () => {
    setSelectedChatId(null);
    setCurrentView('matches');
  };

  const renderContent = () => {
    switch (currentView) {
      case 'discover':
        return <SwipeInterface />;
      case 'matches':
        return <MatchesList onChatClick={handleChatClick} />;
      case 'chat':
        return <ChatInterface matchId={selectedChatId} onBack={handleBackToMatches} />;
      case 'profile':
        return <ProfilePage />;
      default:
        return <SwipeInterface />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 p-4">
        <div className="flex items-center justify-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-red-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">🔥</span>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-red-600 bg-clip-text text-transparent">
              Spark
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {renderContent()}
      </main>

      {/* Navigation */}
      {currentView !== 'chat' && (
        <Navigation currentView={currentView} onViewChange={setCurrentView} />
      )}

      <Toaster />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/*" element={<MainApp />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;