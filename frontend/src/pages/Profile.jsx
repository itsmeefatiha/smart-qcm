import { useState, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI } from '../services/api';

const Profile = () => {
  const { user, setUser } = useAuth(); 
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [imageTimestamp, setImageTimestamp] = useState(Date.now());

  const handleImageClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await userAPI.uploadProfileImage(formData);
      
      const updatedUser = { 
        ...user, 
        profile_image_url: response.data.image_url 
      };
      
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      // Update timestamp to force image refresh
      setImageTimestamp(Date.now());
      
      alert('Profile picture updated successfully!');
    } catch (error) {
      console.error(error);
      alert('Failed to upload image.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Profile</h1>
        <p className="text-gray-600">View your account information</p>
      </div>

      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 h-32"></div>

        <div className="px-8 pb-8">
          <div className="flex items-end -mt-16 mb-6">
            <div className="relative group">
              
              {/* --- PROFILE IMAGE CONTAINER --- */}
              <div 
                className="w-32 h-32 rounded-full bg-white border-4 border-white shadow-lg flex items-center justify-center overflow-hidden cursor-pointer relative"
                onClick={handleImageClick}
              >
                {user?.profile_image_url ? (
                  <img 
                    key={imageTimestamp}
                    src={`${user.profile_image_url}?t=${imageTimestamp}`} 
                    alt="Profile" 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null; 
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
                    <span className="text-4xl font-bold text-white">
                      {user?.first_name?.[0]}{user?.last_name?.[0]}
                    </span>
                  </div>
                )}
                
                {/* Transparent Overlay for hover effect */}
                <div className="absolute inset-0 bg-transparent group-hover:bg-black group-hover:bg-opacity-30 transition-all duration-200 flex items-center justify-center">
                  <svg className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
              </div>

              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
                accept="image/*"
              />
              
              {uploading && (
                <div className="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                </div>
              )}
            </div>
          </div>

          {/* --- INFO SECTION: Stacked Layout --- */}
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {user?.first_name} {user?.last_name}
              </h2>
              <p className="text-gray-600 capitalize">{user?.role}</p>
            </div>

            {/* Changed from GRID to Vertical Stack (space-y-4) */}
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-6 w-full">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Email Address</h3>
                <p className="text-lg text-gray-900">{user?.email}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 w-full">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Account Type</h3>
                <p className="text-lg text-gray-900 capitalize">{user?.role}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 w-full">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Member Since</h3>
                <p className="text-lg text-gray-900">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  }) : 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-white rounded-xl shadow-md p-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Account Information</h2>
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-gray-600">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
            <span>Account is active and verified</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;