import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { examAPI } from '../services/api';

const TakeExam = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const examData = location.state?.examData;

  const [currentQuestion, setCurrentQuestion] = useState(
    examData?.exam_config?.start_at_index || 0
  );
  const [answers, setAnswers] = useState({});
  
  // NEW: Initialize with per-question time, not total time
  const [timeLeft, setTimeLeft] = useState(
    examData?.exam_config?.initial_question_time || examData?.exam_config?.seconds_per_question || 60
  );
  
  const [submitting, setSubmitting] = useState(false);

  // --- 1. VALIDATION ---
  useEffect(() => {
    if (!examData) {
      navigate('/active-exams');
    }
  }, [examData, navigate]);

  // --- 2. TIMER LOGIC (Per Question) ---
  useEffect(() => {
    if (!examData) return;

    // Reset timer whenever we switch to a new question
    setTimeLeft(examData.exam_config.seconds_per_question);

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleTimeUp(); // Trigger auto-advance
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [currentQuestion]); // <--- Dependency: Re-run when question changes

  // --- 3. AUTO-ADVANCE LOGIC ---
  const handleTimeUp = () => {
    const questions = examData.qcm.questions;
    
    if (currentQuestion < questions.length - 1) {
      // Move to next question automatically
      setCurrentQuestion((prev) => prev + 1);
    } else {
      // If it was the last question, auto-submit
      handleSubmit();
    }
  };

  const handleAnswerSelect = (questionId, choiceIndex) => {
    setAnswers({
      ...answers,
      [questionId]: choiceIndex,
    });
  };

  const handleNext = () => {
    // Manual click on "Next"
    if (currentQuestion < examData.qcm.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handleSubmit = async () => {
    if (submitting) return;
    setSubmitting(true);

    const questions = examData.qcm.questions;
    const answersArray = questions.map((q) => ({
      question_id: q.id,
      selected_index: answers[q.id] !== undefined ? answers[q.id] : 0, // Default to 0 if skipped
    }));

    try {
      const response = await examAPI.submit({
        attempt_id: examData.attempt_id, // Fixed the previous error here too
        answers: answersArray,
      });
      navigate('/exam-result', { state: { result: response.data } });
    } catch (err) {
      console.error("Submission Error:", err);
      alert('Failed to submit exam. Check console.');
      setSubmitting(false);
    }
  };

  if (!examData) return null;

  const questions = examData.qcm.questions || [];
  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  // Format time (MM:SS)
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* HEADER */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-xl font-bold text-gray-900">{examData.qcm.title}</h1>
              <p className="text-sm text-gray-600">
                Question {currentQuestion + 1} of {questions.length}
              </p>
            </div>
            <div className="text-right">
              {/* Timer turns red when under 10 seconds */}
              <div className={`text-2xl font-bold ${timeLeft < 10 ? 'text-red-600 animate-pulse' : 'text-gray-900'}`}>
                {formatTime(timeLeft)}
              </div>
              <p className="text-sm text-gray-600">Time for this Question</p>
            </div>
          </div>
          {/* Progress Bar */}
          <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
            <div className="bg-primary-600 h-2 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
          </div>
        </div>
      </div>

      {/* QUESTION AREA */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentQ && (
          <div className="bg-white rounded-xl shadow-md p-8 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">{currentQ.text}</h2>

            <div className="space-y-3">
              {currentQ.choices.map((choice, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswerSelect(currentQ.id, index)}
                  className={`w-full text-left p-4 rounded-lg border-2 transition ${
                    answers[currentQ.id] === index
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300 bg-white'
                  }`}
                >
                  <div className="flex items-center">
                    <div className={`w-6 h-6 rounded-full border-2 mr-4 flex items-center justify-center ${
                      answers[currentQ.id] === index ? 'border-primary-600 bg-primary-600' : 'border-gray-300'
                    }`}>
                      {answers[currentQ.id] === index && <div className="w-2 h-2 bg-white rounded-full" />}
                    </div>
                    <span className="text-gray-900">{choice.text}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* CONTROLS - "Previous" Button REMOVED */}
        <div className="flex justify-end items-center">
          {currentQuestion < questions.length - 1 ? (
            <button
              onClick={handleNext}
              className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-8 rounded-lg transition"
            >
              Next Question
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-8 rounded-lg transition"
            >
              {submitting ? 'Submitting...' : 'Finish Exam'}
            </button>
          )}
        </div>

        {/* NAVIGATOR - LOCKED for Past Questions */}
        <div className="mt-6 bg-white rounded-xl shadow-md p-6">
            <p className="text-sm text-gray-500 mb-2">Progress (Cannot go back)</p>
            <div className="flex flex-wrap gap-2">
                {questions.map((q, index) => {
                    // Logic to style bubbles: 
                    // Green = Answered & Passed
                    // Gray = Future
                    // Blue = Current
                    let statusClass = "bg-gray-100 text-gray-400"; // Default: Future
                    
                    if (index === currentQuestion) {
                        statusClass = "bg-blue-600 text-white ring-2 ring-blue-300"; // Current
                    } else if (index < currentQuestion) {
                        // Past question
                        statusClass = answers[q.id] !== undefined 
                            ? "bg-green-100 text-green-700 border border-green-500" // Answered
                            : "bg-red-100 text-red-700 border border-red-500"; // Skipped/Missed
                    }

                    return (
                        <div key={q.id} className={`w-10 h-10 flex items-center justify-center rounded-lg font-semibold ${statusClass}`}>
                            {index + 1}
                        </div>
                    );
                })}
            </div>
        </div>
      </div>
    </div>
  );
};

export default TakeExam;