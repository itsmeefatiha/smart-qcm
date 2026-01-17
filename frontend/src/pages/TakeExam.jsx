import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { examAPI } from '../services/api';

const TakeExam = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const examData = location.state?.examData;

  // Initialize with backend-calculated values
  const initialQuestionIndex = examData?.exam_config?.start_at_index ?? 0;
  const initialTimeLeft = examData?.exam_config?.initial_question_time ?? examData?.exam_config?.seconds_per_question ?? 60;
  // Use exam_start_time if available (new), otherwise fall back to started_at (backward compatibility)
  const examStartTime = examData?.exam_config?.exam_start_time 
    ? new Date(examData.exam_config.exam_start_time)
    : (examData?.exam_config?.started_at ? new Date(examData.exam_config.started_at) : null);
  const secondsPerQuestion = examData?.exam_config?.seconds_per_question ?? 60;
  
  // Load saved answers from backend if available
  // Convert question IDs from strings to integers
  const savedAnswers = examData?.saved_answers || {};
  const initialAnswers = Object.keys(savedAnswers).reduce((acc, key) => {
    acc[parseInt(key)] = savedAnswers[key];
    return acc;
  }, {});
  const initialAnsweredQuestions = new Set(Object.keys(savedAnswers).map(id => parseInt(id)));
  
  const [currentQuestion, setCurrentQuestion] = useState(initialQuestionIndex);
  const [answers, setAnswers] = useState(initialAnswers);
  const [lockedAnswers, setLockedAnswers] = useState({}); // Track which questions have timed out and answers are locked
  const [answeredQuestions, setAnsweredQuestions] = useState(initialAnsweredQuestions); // Track which questions were actually answered by student
  const [timeLeft, setTimeLeft] = useState(initialTimeLeft);
  const [submitting, setSubmitting] = useState(false);
  const [savingAnswer, setSavingAnswer] = useState(false);
  const [isWaitingForNext, setIsWaitingForNext] = useState(false); // Show waiting message when time is up
  
  // Use ref to track if component is mounted and to avoid stale closures
  const examDataRef = useRef(examData);
  const currentQuestionRef = useRef(currentQuestion);
  const answersRef = useRef(answers);
  const lockedAnswersRef = useRef(lockedAnswers);
  const answeredQuestionsRef = useRef(answeredQuestions);
  const submittingRef = useRef(submitting);
  const handleSubmitRef = useRef(null);
  const examStartTimeRef = useRef(examStartTime);
  const secondsPerQuestionRef = useRef(secondsPerQuestion);
  
  useEffect(() => {
    examDataRef.current = examData;
    currentQuestionRef.current = currentQuestion;
    answersRef.current = answers;
    lockedAnswersRef.current = lockedAnswers;
    answeredQuestionsRef.current = answeredQuestions;
    submittingRef.current = submitting;
    examStartTimeRef.current = examStartTime;
    secondsPerQuestionRef.current = secondsPerQuestion;
  }, [examData, currentQuestion, answers, lockedAnswers, answeredQuestions, submitting, examStartTime, secondsPerQuestion]);

  // --- 1. VALIDATION ---
  useEffect(() => {
    if (!examData) {
      navigate('/active-exams');
    }
  }, [examData, navigate]);

  // Define handleSubmit first so it can be referenced
  const handleSubmit = useCallback(async () => {
    if (submittingRef.current) return;
    setSubmitting(true);
    submittingRef.current = true;

    const questions = examDataRef.current?.qcm?.questions || [];
    // Use locked answers (which include answers locked when time ran out)
    // For unanswered questions, default to 0 (first choice)
    const answersArray = questions.map((q) => ({
      question_id: q.id,
      selected_index: lockedAnswersRef.current[q.id] !== undefined && lockedAnswersRef.current[q.id] !== null
        ? lockedAnswersRef.current[q.id]  // Use locked answer if available
        : (answersRef.current[q.id] !== undefined ? answersRef.current[q.id] : 0), // Use current answer or default to 0
    }));

    try {
      const response = await examAPI.submit({
        attempt_id: examDataRef.current?.attempt_id,
        answers: answersArray,
      });
      navigate('/exam-result', { state: { result: response.data } });
    } catch (err) {
      console.error("Submission Error:", err);
      alert('Failed to submit exam. Check console.');
      setSubmitting(false);
      submittingRef.current = false;
    }
  }, [navigate]);

  // Store handleSubmit in ref for use in timer
  useEffect(() => {
    handleSubmitRef.current = handleSubmit;
  }, [handleSubmit]);

  // --- 2. CONTINUOUS TIME CALCULATION (Based on elapsed time since exam started) ---
  useEffect(() => {
    if (!examData || !examStartTimeRef.current) return;

    const questions = examData.qcm?.questions || [];
    const totalQuestions = questions.length;
    
    // Function to calculate current question and time left based on elapsed time
    const calculateCurrentState = () => {
      const now = new Date();
      const examStartTime = examStartTimeRef.current;
      const secondsPerQuestion = secondsPerQuestionRef.current;
      
      if (!examStartTime) return { questionIndex: 0, timeLeft: secondsPerQuestion };
      
      // Calculate elapsed time in seconds since EXAM STARTED (not when student joined)
      const elapsedSeconds = Math.floor((now - examStartTime) / 1000);
      
      // Calculate which question we should be on
      const calculatedQuestionIndex = Math.floor(elapsedSeconds / secondsPerQuestion);
      
      // Calculate time left for current question
      const timeIntoCurrentQuestion = elapsedSeconds % secondsPerQuestion;
      const calculatedTimeLeft = secondsPerQuestion - timeIntoCurrentQuestion;
      
      return {
        questionIndex: Math.min(calculatedQuestionIndex, totalQuestions - 1),
        timeLeft: Math.max(0, calculatedTimeLeft)
      };
    };

    // Update state immediately
    const currentState = calculateCurrentState();
    setCurrentQuestion(currentState.questionIndex);
    currentQuestionRef.current = currentState.questionIndex;
    setTimeLeft(currentState.timeLeft);
    
    // Initialize locked answers for questions that have already passed
    // (in case student joins late)
    // Only questions that were explicitly saved (in answeredQuestions) count as answered
    const initialLocked = {};
    for (let i = 0; i < currentState.questionIndex; i++) {
      const q = questions[i];
      if (q) {
        // Check if student has a SAVED answer for this question (not just selected)
        // answeredQuestionsRef only contains questions that were explicitly saved
        if (answeredQuestionsRef.current.has(q.id)) {
          initialLocked[q.id] = answersRef.current[q.id];
        } else {
          initialLocked[q.id] = null; // Mark as missed (not saved)
        }
      }
    }
    if (Object.keys(initialLocked).length > 0) {
      setLockedAnswers(initialLocked);
      lockedAnswersRef.current = initialLocked;
    }

    // Set up interval to continuously recalculate (every second)
    const timer = setInterval(() => {
      const state = calculateCurrentState();
      
      // Always update time left based on elapsed time
      setTimeLeft(state.timeLeft);
      
      // Lock answer for previous question if we've moved past it
      if (state.questionIndex > currentQuestionRef.current) {
        // Lock the answer for the question we just left
        const previousQuestion = questions[currentQuestionRef.current];
        if (previousQuestion) {
          setLockedAnswers((prev) => {
            const updated = { ...prev };
            // Only lock if student actually SAVED the answer (not just selected it)
            // Check if it's in answeredQuestions (which only includes saved answers)
            if (answeredQuestionsRef.current.has(previousQuestion.id)) {
              updated[previousQuestion.id] = answersRef.current[previousQuestion.id];
            } else {
              // Mark as missed (student selected but didn't save, or didn't select at all)
              updated[previousQuestion.id] = null; // Use null to indicate missed
            }
            lockedAnswersRef.current = updated;
            return updated;
          });
        }
      }
      
      // Check if time is up for current question
      if (state.timeLeft <= 0) {
        // Lock the answer for current question
        const currentQ = questions[state.questionIndex];
        if (currentQ && !lockedAnswersRef.current[currentQ.id]) {
          setLockedAnswers((prev) => {
            const updated = { ...prev };
            // Only lock if student actually SAVED the answer (not just selected it)
            // Check if it's in answeredQuestions (which only includes saved answers)
            if (answeredQuestionsRef.current.has(currentQ.id)) {
              updated[currentQ.id] = answersRef.current[currentQ.id];
            } else {
              // Mark as missed (student selected but didn't save, or didn't select at all)
              updated[currentQ.id] = null; // Use null to indicate missed
            }
            lockedAnswersRef.current = updated;
            return updated;
          });
        }
        
        // Show waiting message if not last question
        if (state.questionIndex < totalQuestions - 1) {
          setIsWaitingForNext(true);
        }
      } else {
        setIsWaitingForNext(false);
      }
      
      // Auto-advance if calculated question is ahead (time passed)
      // This ensures time passes fluently regardless of refreshes or manual actions
      if (state.questionIndex > currentQuestionRef.current) {
        if (state.questionIndex >= totalQuestions) {
          // All questions completed, auto-submit
          setIsWaitingForNext(false);
          if (handleSubmitRef.current) {
            handleSubmitRef.current();
          }
        } else {
          // Auto-advance to the correct question based on elapsed time
          setCurrentQuestion(state.questionIndex);
          currentQuestionRef.current = state.questionIndex;
          setIsWaitingForNext(false);
        }
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [examData]);

  const handleAnswerSelect = (questionId, choiceIndex) => {
    // Don't allow changing answer if time is up for this question
    if (lockedAnswersRef.current[questionId] !== undefined) {
      return; // Answer is locked, cannot change
    }
    
    // Don't allow changing answer if time is up (timeLeft <= 0)
    if (timeLeft <= 0) {
      return; // Time is up, answer is locked
    }
    
    // Update local state only (don't save to backend or mark as answered yet)
    // Student must click "Save Answer" to actually save it
    setAnswers({
      ...answers,
      [questionId]: choiceIndex,
    });
  };

  // Handle saving current answer (without advancing)
  const handleSaveAnswer = useCallback(async () => {
    const questions = examDataRef.current?.qcm?.questions || [];
    const currentQId = questions[currentQuestion]?.id;
    if (!currentQId || savingAnswer) return;
    
    const currentAnswer = answersRef.current[currentQId];
    if (currentAnswer === undefined) {
      alert('Please select an answer before saving.');
      return;
    }
    
    setSavingAnswer(true);
    
    try {
      // Save to backend
      await examAPI.saveAnswer({
        attempt_id: examDataRef.current?.attempt_id,
        question_id: currentQId,
        selected_index: currentAnswer
      });
      
      // Mark as answered by student
      setAnsweredQuestions((prev) => {
        const updated = new Set(prev);
        updated.add(currentQId);
        answeredQuestionsRef.current = updated;
        return updated;
      });
      
      // Show success message briefly
      const successMsg = document.createElement('div');
      successMsg.className = 'fixed top-20 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
      successMsg.textContent = 'Answer saved!';
      document.body.appendChild(successMsg);
      setTimeout(() => {
        document.body.removeChild(successMsg);
      }, 2000);
    } catch (err) {
      console.error("Save Error:", err);
      alert('Failed to save answer. Check console.');
    } finally {
      setSavingAnswer(false);
    }
  }, [currentQuestion, savingAnswer]);


  if (!examData) return null;

  const questions = examData.qcm.questions || [];
  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  
  // Check if current question answer is locked (time has run out)
  const isCurrentQuestionLocked = currentQ ? (lockedAnswers[currentQ.id] !== undefined || timeLeft <= 0) : false;
  
  // Get the answer to display (locked answer takes precedence, but ignore null which means missed)
  const currentAnswer = currentQ 
    ? (lockedAnswers[currentQ.id] !== undefined && lockedAnswers[currentQ.id] !== null 
        ? lockedAnswers[currentQ.id] 
        : answers[currentQ.id])
    : undefined;

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

            {isWaitingForNext && timeLeft <= 0 && currentQuestion < questions.length - 1 ? (
              <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6 text-center">
                <p className="text-yellow-800 font-semibold text-lg mb-2">Time is up for this question!</p>
                <p className="text-yellow-700">Your answer has been locked. Waiting for next question...</p>
              </div>
            ) : (
              <div className="space-y-3">
                {currentQ.choices.map((choice, index) => {
                  const isSelected = currentAnswer === index;
                  const isDisabled = isCurrentQuestionLocked;
                  
                  return (
                    <button
                      key={index}
                      onClick={() => handleAnswerSelect(currentQ.id, index)}
                      disabled={isDisabled}
                      className={`w-full text-left p-4 rounded-lg border-2 transition ${
                        isSelected
                          ? 'border-primary-600 bg-primary-50'
                          : isDisabled
                          ? 'border-gray-200 bg-gray-50 cursor-not-allowed opacity-60'
                          : 'border-gray-200 hover:border-gray-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center">
                        <div className={`w-6 h-6 rounded-full border-2 mr-4 flex items-center justify-center ${
                          isSelected ? 'border-primary-600 bg-primary-600' : 'border-gray-300'
                        }`}>
                          {isSelected && <div className="w-2 h-2 bg-white rounded-full" />}
                        </div>
                        <span className={`text-gray-900 ${isDisabled ? 'opacity-60' : ''}`}>{choice.text}</span>
                        {isSelected && isDisabled && (
                          <span className="ml-auto text-xs text-gray-500 italic">(Locked)</span>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* CONTROLS - Save Answer button and Final Submit */}
        <div className="flex justify-between items-center">
          {/* Save Answer Button - Only show if question is not locked and answer is selected */}
          {!isCurrentQuestionLocked && currentAnswer !== undefined && currentQuestion < questions.length - 1 ? (
            <button
              onClick={handleSaveAnswer}
              disabled={savingAnswer}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition"
            >
              {savingAnswer ? 'Saving...' : 'Save Answer'}
            </button>
          ) : (
            <div></div>
          )}
          
          {/* Final Submit Button - Only show on last question when time is up */}
          {currentQuestion >= questions.length - 1 && timeLeft <= 0 ? (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-8 rounded-lg transition"
            >
              {submitting ? 'Submitting...' : 'Submit Exam'}
            </button>
          ) : isWaitingForNext ? (
            <div className="text-gray-500 text-sm italic">
              Time is up! Waiting for next question to appear automatically...
            </div>
          ) : (
            <div></div>
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
                        // Past question - only show green if actually SAVED by student
                        // answeredQuestions only contains questions that were explicitly saved
                        const wasAnswered = answeredQuestions.has(q.id);
                        statusClass = wasAnswered 
                            ? "bg-green-100 text-green-700 border border-green-500" // Answered & Saved
                            : "bg-red-100 text-red-700 border border-red-500"; // Skipped/Missed (not saved)
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