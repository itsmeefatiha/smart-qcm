import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { qcmAPI, examAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const QcmDetails = () => {
  const { qcmId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [qcm, setQcm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleting, setDeleting] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);
  const [editFormData, setEditFormData] = useState({ text: '', choices: [] });

  useEffect(() => {
    fetchQcm();
  }, [qcmId]);

  const fetchQcm = async () => {
    try {
      const response = await qcmAPI.getById(qcmId);
      setQcm(response.data);
    } catch (err) {
      setError('Failed to load QCM details');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this QCM? This action cannot be undone.')) {
      return;
    }

    setDeleting(true);
    try {
      await qcmAPI.delete(qcmId);
      navigate('/my-qcms', { state: { message: 'QCM deleted successfully' } });
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to delete QCM';
      alert(errorMsg);
    } finally {
      setDeleting(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await qcmAPI.downloadPDF(qcmId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `exam_${qcmId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download PDF');
    }
  };

  const startEdit = (question) => {
    setEditingQuestion(question.id);
    setEditFormData({
      text: question.text,
      choices: question.choices,
    });
  };

  const handleEditChange = (field, value) => {
    setEditFormData({ ...editFormData, [field]: value });
  };

  const handleChoiceChange = (index, field, value) => {
    const newChoices = [...editFormData.choices];
    newChoices[index] = { ...newChoices[index], [field]: value };
    setEditFormData({ ...editFormData, choices: newChoices });
  };

  const handleCorrectAnswerChange = (index) => {
    const newChoices = editFormData.choices.map((choice, i) => ({
      ...choice,
      is_correct: i === index,
    }));
    setEditFormData({ ...editFormData, choices: newChoices });
  };

  const saveEdit = async () => {
    try {
      await qcmAPI.updateQuestion(editingQuestion, editFormData);
      setEditingQuestion(null);
      fetchQcm();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to update question');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !qcm) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error || 'QCM not found'}
        </div>
        <Link
          to="/my-qcms"
          className="text-primary-600 hover:text-primary-700 font-medium"
        >
          Back to My QCMs
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <Link
          to="/my-qcms"
          className="text-primary-600 hover:text-primary-700 font-medium mb-4 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to My QCMs
        </Link>

        <div className="flex justify-between items-start mt-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{qcm.title}</h1>
            <div className="flex gap-2">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 capitalize">
                {qcm.level}
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                {qcm.questions?.length || 0} Questions
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleDownloadPDF}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF
            </button>
            {user?.role === 'professor' && (
              <>
                <Link
                  to={`/create-exam/${qcmId}`}
                  className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-4 rounded-lg transition"
                >
                  Create Exam Session
                </Link>
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
                >
                  {deleting ? 'Deleting...' : 'Delete QCM'}
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {qcm.questions?.map((question, index) => (
          <div key={question.id} className="bg-white rounded-xl shadow-md p-6">
            {editingQuestion === question.id ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Question Text
                  </label>
                  <textarea
                    value={editFormData.text}
                    onChange={(e) => handleEditChange('text', e.target.value)}
                    rows="3"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Choices (Select the correct one)
                  </label>
                  {editFormData.choices.map((choice, idx) => (
                    <div key={idx} className="flex items-center gap-3">
                      <input
                        type="radio"
                        checked={choice.is_correct}
                        onChange={() => handleCorrectAnswerChange(idx)}
                        className="w-5 h-5 text-primary-600"
                      />
                      <input
                        type="text"
                        value={choice.text}
                        onChange={(e) => handleChoiceChange(idx, 'text', e.target.value)}
                        className="flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                  ))}
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={saveEdit}
                    className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition"
                  >
                    Save Changes
                  </button>
                  <button
                    onClick={() => setEditingQuestion(null)}
                    className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded-lg transition"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-bold text-gray-900">
                    Question {index + 1}
                  </h3>
                  {user?.role === 'professor' && (
                    <button
                      onClick={() => startEdit(question)}
                      className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      Edit
                    </button>
                  )}
                </div>

                <p className="text-gray-900 mb-4">{question.text}</p>

                <div className="space-y-2">
                  {question.choices?.map((choice, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border-2 ${
                        choice.is_correct
                          ? 'border-green-500 bg-green-50'
                          : 'border-gray-200 bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="font-semibold text-gray-700">
                          {String.fromCharCode(65 + idx)}.
                        </span>
                        <span className="text-gray-900">{choice.text}</span>
                        {choice.is_correct && (
                          <span className="ml-auto inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Correct Answer
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default QcmDetails;
