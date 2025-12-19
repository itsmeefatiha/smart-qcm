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
          {user?.role === 'professor'
            ? 'Create AI-powered exams and manage your QCMs'
            : 'Take exams and track your progress'}
        </p>
      </div>

      {user?.role === 'professor' ? (
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
              Add course materials for AI exam generation
            </p>
          </Link>

          <Link
            to="/generate-qcm"
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
          >
            <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Generate QCM
            </h3>
            <p className="text-gray-600">
              Use AI to create exams from your documents
            </p>
          </Link>

          <Link
            to="/my-qcms"
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
          >
            <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mb-4">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              My QCMs
            </h3>
            <p className="text-gray-600">
              View and manage your generated exams
            </p>
          </Link>

          <Link
            to="/documents"
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
          >
            <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              My Documents
            </h3>
            <p className="text-gray-600">
              Browse your uploaded course materials
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
              View your account information
            </p>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link
            to="/active-exams"
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-2 border-transparent hover:border-primary-500"
          >
            <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Active Exams
            </h3>
            <p className="text-gray-600">
              View and join available exams
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
              View your account information
            </p>
          </Link>
        </div>
      )}

      <div className="mt-12 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Info</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-primary-600 mb-2 capitalize">{user?.role}</div>
            <div className="text-gray-600">Account Type</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600 mb-2">Active</div>
            <div className="text-gray-600">Status</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-3xl font-bold text-orange-600 mb-2">AI-Powered</div>
            <div className="text-gray-600">Platform</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
