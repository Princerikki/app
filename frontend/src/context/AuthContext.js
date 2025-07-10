import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, userAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token and fetch user data
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getMe()
        .then((userData) => {
          setUser(userData);
          localStorage.setItem('currentUser', JSON.stringify(userData));
        })
        .catch((error) => {
          console.error('Failed to fetch user:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('currentUser');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      const { access_token, user: userData } = response;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('currentUser', JSON.stringify(userData));
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const signup = async (userData) => {
    try {
      const response = await authAPI.signup(userData);
      const { access_token, user: newUser } = response;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('currentUser', JSON.stringify(newUser));
      setUser(newUser);
      
      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Signup failed' 
      };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
  };

  const updateProfile = async (updates) => {
    try {
      const updatedUser = await userAPI.updateProfile(updates);
      setUser(updatedUser);
      localStorage.setItem('currentUser', JSON.stringify(updatedUser));
      return { success: true };
    } catch (error) {
      console.error('Profile update error:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Profile update failed' 
      };
    }
  };

  const value = {
    user,
    login,
    signup,
    logout,
    updateProfile,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};