import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { qcmAPI, examAPI, schoolAPI } from '../services/api';

const CreateExamSession = () => {
  const { qcmId } = useParams();
  const navigate = useNavigate();
  const [qcm, setQcm] = useState(null);
  const [branches, setBranches] = useState([]);

  const [formData, setFormData] = useState({
    description: '',
    start_time: '',
    duration_minutes: 60,
    total_grade: 20,
    branch_id: '',
  });

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [sessionCode, setSessionCode] = useState('');

  useEffect(() => {
    fetchQcm();
    fetchBranches();
  }, [qcmId]);

  const fetchBranches = async () => {
    try {
      const response = await schoolAPI.listBranches();
      setBranches(response.data);
    } catch (err) {
      console.error('Failed to load branches:', err);
    }
  };

  const fetchQcm = async () => {
    try {
      const response = await qcmAPI.getById(qcmId);
      setQcm(response.data);

      // Initialize start_time to current local time for the input
      const now = new Date();
      // Trick to get local ISO string for datetime-local input
      const localIsoString = new Date(now.getTime() - (now.getTimezoneOffset() * 60000))
        .toISOString()
        .slice(0, 16);

      setFormData(prev => ({
        ...prev,
        start_time: localIsoString,
      }));
    } catch (err) {
      setError('Failed to load QCM');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    if (!formData.branch_id) {
      setError('Please select a branch');
      setSubmitting(false);
      return;
    }

    try {
      const response = await examAPI.create({
        qcm_id: parseInt(qcmId),
        description: formData.description,
        start_time: new Date(formData.start_time).toISOString(),
        duration_minutes: parseInt(formData.duration_minutes),
        total_grade: parseInt(formData.total_grade),
        branch_id: parseInt(formData.branch_id),
      });

      setSessionCode(response.data.code);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to create exam session');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // --- SUCCESS VIEW (Displaying Code) ---
  if (sessionCode) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Exam Session Created!</h1>

          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <p className="text-sm text-gray-600 mb-2">Share this code with students:</p>
            <div className="text-5xl font-bold text-primary-600 tracking-wider mb-2">
              {sessionCode}
            </div>
            <p className="text-xs text-gray-500">Students will use this code to join the exam</p>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6 text-left">
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Duration</p>
              <p className="text-lg font-semibold text-gray-900">{formData.duration_minutes} minutes</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Total Grade</p>
              <p className="text-lg font-semibold text-gray-900">{formData.total_grade} points</p>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => navigate('/my-qcms')}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg transition"
            >
              Back to QCMs
            </button>
            <button
              onClick={() => navigate('/professor-dashboard')} // Assuming you have a dashboard
              className="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  // --- FORM VIEW ---
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Exam Session</h1>
        <p className="text-gray-600">Set up a live exam session for students</p>
        {qcm && (
          <div className="mt-4 bg-blue-50 rounded-lg p-4">
            <p className="text-sm text-gray-700">
              <span className="font-semibold">Selected QCM:</span> {qcm.title}
            </p>
            <p className="text-sm text-gray-700">
              <span className="font-semibold">Questions:</span> {qcm.question_count || qcm.questions?.length || 0}
            </p>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-md p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* NEW: Description Field */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Exam Description (Optional)
            </label>
            <textarea
              id="description"
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              placeholder="e.g. Final exam for the Java module. Good luck!"
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 mb-2">
                Start Time *
              </label>
              <input
                id="start_time"
                name="start_time"
                type="datetime-local"
                required
                value={formData.start_time}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
              <p className="mt-1 text-xs text-gray-500">Local time</p>
            </div>

            <div>
              <label htmlFor="duration_minutes" className="block text-sm font-medium text-gray-700 mb-2">
                Duration (minutes) *
              </label>
              <input
                id="duration_minutes"
                name="duration_minutes"
                type="number"
                min="1"
                max="300"
                required
                value={formData.duration_minutes}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
            </div>
          </div>

          <div>
            <label htmlFor="branch_id" className="block text-sm font-medium text-gray-700 mb-2">
              Target Branch *
            </label>
            <select
              id="branch_id"
              name="branch_id"
              required
              value={formData.branch_id}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            >
              <option value="">Select branch...</option>
              {branches.map((branch) => (
                <option key={branch.id} value={branch.id}>
                  {branch.name}
                </option>
              ))}
            </select>
            <p className="mt-2 text-sm text-gray-500">Only students from this branch will see this exam</p>
          </div>

          <div>
            <label htmlFor="total_grade" className="block text-sm font-medium text-gray-700 mb-2">
              Total Grade Score *
            </label>
            <input
              id="total_grade"
              name="total_grade"
              type="number"
              min="1"
              max="100"
              required
              value={formData.total_grade}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
            <p className="mt-2 text-sm text-gray-500">Maximum score for this exam (e.g., 20 or 100)</p>
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={() => navigate('/my-qcms')}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-4 rounded-lg transition duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? 'Creating Session...' : 'Create Session'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateExamSession;