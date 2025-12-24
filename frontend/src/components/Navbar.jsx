import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            {/* Logo Section */}
            <Link to="/dashboard" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span className="text-xl font-bold text-gray-900">SmartQcm</span>
            </Link>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex ml-10 space-x-8">
              <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">
                Dashboard
              </Link>

              {user?.role === 'professor' && (
                <>
                  <Link to="/documents" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">Documents</Link>
                  <Link to="/my-qcms" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">My QCMs</Link>
                  <Link to="/my-exams" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">My Exams</Link>
                </>
              )}

              {user?.role === 'student' && (
                <>
                  <Link to="/active-exams" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">Exams</Link>
                  <Link to="/documents" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">Documents</Link>
                  <Link to="/my-qcms" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">Practice</Link>
                </>
              )}
              {user?.role === 'manager' && (
    <>
      <Link to="/exams/all" className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition">
        Exams
      </Link>
    </>
  )}
            </div>
          </div>

          {/* Desktop Right Side: Profile & Logout */}
          <div className="hidden md:flex items-center gap-6">
            <Link
              to="/profile"
              className="flex items-center gap-3 text-gray-700 hover:text-primary-600 transition group"
            >
              {/* Profile Image */}
              {user?.profile_image_url ? (
                <img 
                  src={`${user.profile_image_url}?t=${new Date().getTime()}`} 
                  alt="Profile" 
                  className="w-9 h-9 rounded-full object-cover border border-gray-200 group-hover:border-primary-500 transition"
                  onError={(e) => { e.target.onerror = null; e.target.style.display = 'none'; }}
                />
              ) : (
                <div className="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition">
                  <span className="text-sm font-semibold text-primary-600">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
              )}
              
              {/* User Name */}
              <span className="text-sm font-medium">{user?.first_name}</span>
            </Link>

            {/* Logout Icon Button (Desktop) */}
            <button
              onClick={handleLogout}
              title="Logout"
              className="p-2 rounded-full text-gray-500 hover:bg-red-50 hover:text-red-600 transition"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-primary-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-4 py-3 space-y-1">
            <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">Dashboard</Link>
            
            {user?.role === 'professor' && (
              <>
                <Link to="/documents" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">Documents</Link>
                <Link to="/my-qcms" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">My QCMs</Link>
                <Link to="/my-exams" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">My Exams</Link>
              </>
            )}

            {user?.role === 'student' && (
              <>
                <Link to="/active-exams" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">Exams</Link>
                <Link to="/documents" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">Documents</Link>
                <Link to="/my-qcms" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">Practice</Link>
              </>
            )}

            <div className="border-t border-gray-100 my-2 pt-2">
              <Link to="/profile" onClick={() => setMobileMenuOpen(false)} className="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg flex items-center gap-2">
                {/* Mobile Profile Icon */}
                <div className="w-6 h-6 rounded-full bg-primary-100 flex items-center justify-center text-xs font-bold text-primary-600">
                  {user?.first_name?.[0]}
                </div>
                Profile
              </Link>
              <button
                onClick={() => { setMobileMenuOpen(false); handleLogout(); }}
                className="w-full text-left px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;