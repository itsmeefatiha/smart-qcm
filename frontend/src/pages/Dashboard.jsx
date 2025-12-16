import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.first_name}!
        </h1>
        <p className="text-gray-600">
          Manage your educational documents and course materials
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link
          to="/upload"
          className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
            <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Upload Document
          </h3>
          <p className="text-gray-600">
            Add new course materials, PDFs, or documents to your collection
          </p>
        </Link>

        <Link
          to="/documents"
          className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            My Documents
          </h3>
          <p className="text-gray-600">
            View and manage all your uploaded documents
          </p>
        </Link>

        <Link
          to="/profile"
          className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-orange-100 rounded-lg mb-4">
            <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            My Profile
          </h3>
          <p className="text-gray-600">
            View your account information and settings
          </p>
        </Link>
      </div>

      <div className="mt-12 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Stats</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-primary-600 mb-2">-</div>
            <div className="text-gray-600">Total Documents</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600 mb-2">{user?.role}</div>
            <div className="text-gray-600">Account Type</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-orange-600 mb-2">Active</div>
            <div className="text-gray-600">Status</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
