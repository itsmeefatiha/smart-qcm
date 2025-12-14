import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user } = useAuth();

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
            <div className="w-32 h-32 rounded-full bg-white border-4 border-white shadow-lg flex items-center justify-center">
              <div className="w-28 h-28 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
                <span className="text-4xl font-bold text-white">
                  {user?.first_name?.[0]}{user?.last_name?.[0]}
                </span>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {user?.first_name} {user?.last_name}
              </h2>
              <p className="text-gray-600 capitalize">{user?.role}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Email Address</h3>
                <p className="text-lg text-gray-900">{user?.email}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Account Type</h3>
                <p className="text-lg text-gray-900 capitalize">{user?.role}</p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Member Since</h3>
                <p className="text-lg text-gray-900">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  }) : 'N/A'}
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-sm font-medium text-gray-500 mb-2">User ID</h3>
                <p className="text-lg text-gray-900">{user?.id}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-white rounded-xl shadow-md p-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Account Information</h2>
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-gray-600">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Account is active and verified</span>
          </div>
          <div className="flex items-center gap-3 text-gray-600">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Email notifications enabled</span>
          </div>
          <div className="flex items-center gap-3 text-gray-600">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Document upload permissions granted</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
