import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Avatar, AvatarImage, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';
import { Settings, Camera, Plus, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../hooks/use-toast';

const ProfilePage = () => {
  const { user, updateProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    name: user?.name || '',
    age: user?.age || '',
    bio: user?.bio || '',
    occupation: user?.occupation || '',
    education: user?.education || '',
    interests: user?.interests || []
  });
  const [newInterest, setNewInterest] = useState('');
  const { toast } = useToast();

  const handleSave = () => {
    updateProfile(editData);
    setIsEditing(false);
    toast({
      title: "Profile updated! ✨",
      description: "Your changes have been saved.",
    });
  };

  const handleAddInterest = () => {
    if (newInterest.trim() && !editData.interests.includes(newInterest.trim())) {
      setEditData({
        ...editData,
        interests: [...editData.interests, newInterest.trim()]
      });
      setNewInterest('');
    }
  };

  const handleRemoveInterest = (interest) => {
    setEditData({
      ...editData,
      interests: editData.interests.filter(i => i !== interest)
    });
  };

  return (
    <div className="p-4 max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Profile</h1>
        <Button
          variant="outline"
          onClick={() => setIsEditing(!isEditing)}
          className="flex items-center space-x-2"
        >
          <Settings className="w-4 h-4" />
          <span>{isEditing ? 'Cancel' : 'Edit'}</span>
        </Button>
      </div>

      {/* Profile Photo Section */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col items-center space-y-4">
            <Avatar className="w-32 h-32">
              <AvatarImage src={user?.photos?.[0]} alt={user?.name} />
              <AvatarFallback className="text-2xl">{user?.name?.[0]}</AvatarFallback>
            </Avatar>
            {isEditing && (
              <Button variant="outline" className="flex items-center space-x-2">
                <Camera className="w-4 h-4" />
                <span>Change Photo</span>
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Basic Info */}
      <Card>
        <CardHeader>
          <CardTitle>Basic Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="name">Name</Label>
              {isEditing ? (
                <Input
                  id="name"
                  value={editData.name}
                  onChange={(e) => setEditData({...editData, name: e.target.value})}
                />
              ) : (
                <p className="text-lg font-semibold">{user?.name}</p>
              )}
            </div>
            <div>
              <Label htmlFor="age">Age</Label>
              {isEditing ? (
                <Input
                  id="age"
                  type="number"
                  value={editData.age}
                  onChange={(e) => setEditData({...editData, age: e.target.value})}
                />
              ) : (
                <p className="text-lg font-semibold">{user?.age}</p>
              )}
            </div>
          </div>
          
          <div>
            <Label htmlFor="bio">Bio</Label>
            {isEditing ? (
              <Textarea
                id="bio"
                value={editData.bio}
                onChange={(e) => setEditData({...editData, bio: e.target.value})}
                placeholder="Tell people about yourself..."
                className="min-h-20"
              />
            ) : (
              <p className="text-gray-600">{user?.bio}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Work & Education */}
      <Card>
        <CardHeader>
          <CardTitle>Work & Education</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="occupation">Occupation</Label>
            {isEditing ? (
              <Input
                id="occupation"
                value={editData.occupation}
                onChange={(e) => setEditData({...editData, occupation: e.target.value})}
              />
            ) : (
              <p className="text-lg font-semibold">{user?.occupation}</p>
            )}
          </div>
          
          <div>
            <Label htmlFor="education">Education</Label>
            {isEditing ? (
              <Input
                id="education"
                value={editData.education}
                onChange={(e) => setEditData({...editData, education: e.target.value})}
              />
            ) : (
              <p className="text-lg font-semibold">{user?.education}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Interests */}
      <Card>
        <CardHeader>
          <CardTitle>Interests</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {(isEditing ? editData.interests : user?.interests || []).map((interest, index) => (
              <Badge key={index} variant="secondary" className="flex items-center space-x-1">
                <span>{interest}</span>
                {isEditing && (
                  <button
                    onClick={() => handleRemoveInterest(interest)}
                    className="ml-1 hover:text-red-500"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </Badge>
            ))}
          </div>
          
          {isEditing && (
            <div className="flex space-x-2">
              <Input
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                placeholder="Add an interest..."
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddInterest())}
              />
              <Button onClick={handleAddInterest} variant="outline">
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Preferences */}
      <Card>
        <CardHeader>
          <CardTitle>Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Age Range</Label>
              <p className="text-lg font-semibold">{user?.preferences?.minAge || 18} - {user?.preferences?.maxAge || 35}</p>
            </div>
            <div>
              <Label>Max Distance</Label>
              <p className="text-lg font-semibold">{user?.preferences?.maxDistance || 25} km</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      {isEditing && (
        <Button
          onClick={handleSave}
          className="w-full bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white"
        >
          Save Changes
        </Button>
      )}
    </div>
  );
};

export default ProfilePage;