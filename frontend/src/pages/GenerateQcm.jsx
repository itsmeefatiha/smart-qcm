import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { documentAPI, qcmAPI } from '../services/api';

const GenerateQcm = () => {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  const [formData, setFormData] = useState({
    document_id: '',
    num_questions: 10,
    level: 'medium',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await documentAPI.list();
      setDocuments(response.data);
    } catch (err) {
      setError('Failed to load documents');
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
    setLoading(true);
    setError('');
    setSuccess('');

    if (!formData.document_id) {
      setError('Please select a document');
      setLoading(false);
      return;
    }

    try {
      const response = await qcmAPI.generate({
        document_id: parseInt(formData.document_id),
        num_questions: parseInt(formData.num_questions),
        level: formData.level,
      });

      setSuccess(`QCM generated successfully! (ID: ${response.data.qcm_id})`);
      setTimeout(() => {
        navigate('/my-qcms');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate QCM. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Generate QCM</h1>
        <p className="text-gray-600">Use AI to automatically generate exam questions from your documents</p>
      </div>

      <div className="bg-white rounded-xl shadow-md p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
              {success}
            </div>
          )}

          <div>
            <label htmlFor="document_id" className="block text-sm font-medium text-gray-700 mb-2">
              Select Document *
            </label>
            <select
              id="document_id"
              name="document_id"
              required
              value={formData.document_id}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            >
              <option value="">Choose a document...</option>
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.filename} - {doc.module}
                </option>
              ))}
            </select>
            {documents.length === 0 && (
              <p className="mt-2 text-sm text-gray-500">
                No documents found. Please upload a document first.
              </p>
            )}
          </div>

          <div>
            <label htmlFor="num_questions" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Questions
            </label>
            <input
              id="num_questions"
              name="num_questions"
              type="number"
              min="1"
              max="50"
              value={formData.num_questions}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
            <p className="mt-2 text-sm text-gray-500">Choose between 1 and 50 questions</p>
          </div>

          <div>
            <label htmlFor="level" className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              id="level"
              name="level"
              value={formData.level}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-800">
                <p className="font-semibold mb-1">How it works:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>AI analyzes your document content</li>
                  <li>Generates multiple-choice questions</li>
                  <li>Takes about 30-60 seconds depending on document size</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-4 rounded-lg transition duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || documents.length === 0}
              className="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Generating...' : 'Generate QCM'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default GenerateQcm;
