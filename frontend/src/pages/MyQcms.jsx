import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { qcmAPI } from '../services/api';

const MyQcms = () => {
  const navigate = useNavigate();
  const [qcms, setQcms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchQcms();
  }, []);

  const fetchQcms = async () => {
    try {
      const response = await qcmAPI.list();
      setQcms(response.data);
    } catch (err) {
      setError('Failed to load QCMs');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSession = (qcmId) => {
    navigate(`/create-exam/${qcmId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My QCMs</h1>
          <p className="text-gray-600">View and manage your generated exams</p>
        </div>
        <Link
          to="/generate-qcm"
          className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Generate New QCM
        </Link>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {qcms.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-12 text-center">
          <svg
            className="mx-auto h-16 w-16 text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No QCMs yet</h3>
          <p className="text-gray-600 mb-6">Generate your first AI-powered exam</p>
          <Link
            to="/generate-qcm"
            className="inline-block bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200"
          >
            Generate QCM
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {qcms.map((qcm) => (
            <div
              key={qcm.id}
              className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border border-gray-200"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{qcm.title}</h3>
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
                      {qcm.level}
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {qcm.question_count} Questions
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-sm text-gray-500 mb-4">
                Created {new Date(qcm.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                })}
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleCreateSession(qcm.id)}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium py-2 px-3 rounded-lg transition"
                >
                  Create Session
                </button>
                <Link
                  to={`/qcm/${qcm.id}`}
                  className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium py-2 px-3 rounded-lg transition text-center"
                >
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyQcms;
