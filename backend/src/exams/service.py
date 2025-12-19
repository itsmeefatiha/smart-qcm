from .repository import ExamRepository
from .models import ExamSession, StudentAnswer
from src.qcm.repository import QCMRepository 
from src.qcm.models import Question
from datetime import datetime, timedelta

class ExamService:
    @staticmethod
    def create_exam_session(professor_id, data):
        qcm_id = data.get('qcm_id')
        qcm = QCMRepository.get_by_id(qcm_id)
        if not qcm:
            return None, "QCM not found"
            
        # --- NEW: Date Calculation Logic ---
        try:
            # 1. Parse Start Time (Assuming ISO format string from Frontend)
            # Example: "2025-12-20T10:00"
            start_dt = datetime.fromisoformat(data['start_time'])
            
            # 2. Get Duration
            duration = int(data.get('duration_minutes', 60))
            
            # 3. Calculate End Time automatically
            end_dt = start_dt + timedelta(minutes=duration)
            
            # 4. Update data dict for repository
            data['start_time'] = start_dt
            data['end_time'] = end_dt # Pass the calculated object
            data['duration_minutes'] = duration
            
        except ValueError:
            return None, "Invalid Date Format. Use ISO format (YYYY-MM-DDTHH:MM)"

        data['total_grade'] = data.get('total_grade', 20)
        data['professor_id'] = professor_id
        
        return ExamRepository.create_session(data), None

    @staticmethod
    def delete_exam_session(professor_id, session_id):
        session = ExamRepository.get_session_by_id(session_id)
        if not session:
            return None, "Exam session not found"
            
        if session.professor_id != professor_id:
            return None, "Unauthorized: You can only delete your own exams."
            
        ExamRepository.delete_session(session)
        return "Exam deleted successfully", None

    @staticmethod
    def get_professor_exams(professor_id):
        """Get list of ALL exams created by this professor"""
        sessions = ExamRepository.get_all_by_professor(professor_id)
        return sessions

    @staticmethod
    def join_exam(student_id, code):
        session = ExamRepository.get_session_by_code(code)
        if not session:
            return None, "Invalid or inactive session code."

        now = datetime.now()
        if now < session.start_time or now > session.end_time:
            return None, "Exam is not currently open."

        # --- GET OR CREATE ATTEMPT ---
        attempt = ExamRepository.get_student_attempt(student_id, session.id)
        if not attempt:
            # First time joining: Timer starts NOW
            attempt = ExamRepository.create_attempt(student_id, session.id)
        
        if attempt.finished_at:
             return None, "You have already submitted this exam."

        # --- THE FIX: CALCULATE CURRENT QUESTION INDEX ---
        
        # 1. Calculate time per question
        question_count = len(session.qcm.questions)
        total_seconds = session.duration_minutes * 60
        seconds_per_question = int(total_seconds / question_count) if question_count > 0 else 0

        # 2. Calculate how much time has passed since they STARTED
        # (This timer kept running even while they were disconnected!)
        elapsed_time = (now - attempt.started_at).total_seconds()
        
        # 3. Determine which question they should be on
        # Example: 300 seconds passed / 60 sec per question = Index 5 (Question 6)
        current_index = int(elapsed_time // seconds_per_question)
        
        # 4. Calculate remaining time for the specific question they landed on
        # Example: 320 seconds passed. 320 % 60 = 20 seconds used. 60 - 20 = 40 seconds left.
        time_left_in_current_question = seconds_per_question - (elapsed_time % seconds_per_question)

        # 5. Check if they ran out of time completely
        if current_index >= question_count:
            # Auto-submit if time is up
            # (You might want to mark it finished in DB here)
            return None, "Time is up! The exam duration has passed."

        return {
            "attempt_id": attempt.id, # Ensure this matches your route expectation
            "qcm": session.qcm.to_dict(), 
            "exam_config": {
                "total_duration": session.duration_minutes,
                "seconds_per_question": seconds_per_question,
                "start_at_index": current_index,          # <--- SEND THIS TO FRONTEND
                "initial_question_time": time_left_in_current_question # <--- AND THIS
            }
        }, None
    
    @staticmethod
    def get_active_sessions_for_student(user_branch=None):
        # Optional: You could filter by the student's branch if you wanted
        now = datetime.now()
        
        # Fetch sessions where Now is between Start and End
        active_sessions = ExamSession.query.filter(
            ExamSession.start_time <= now,
            ExamSession.end_time >= now,
            ExamSession.is_active == True
        ).all()
        
        return active_sessions

    @staticmethod
    def submit_exam(attempt_id, student_answers_payload):
        attempt = ExamRepository.get_attempt(attempt_id)
        if not attempt:
            return None, "Attempt not found"

        if attempt.finished_at:
            return None, "Exam already submitted."

        # --- DYNAMIC SCORING ENGINE ---
        
        # 1. Get total questions count
        total_questions = len(attempt.session.qcm.questions)
        if total_questions == 0:
            return None, "Error: Exam has 0 questions."

        # 2. Calculate weight per question (e.g., 20 / 10 = 2 points each)
        points_per_question = attempt.session.total_grade / total_questions

        correct_count = 0
        answers_to_save = []
        
        for ans_data in student_answers_payload:
            q_id = ans_data.get('question_id')
            idx = ans_data.get('selected_index')
            
            question = Question.query.get(q_id)
            if not question: 
                continue 

            correct_idx = question.get_correct_choice_index()
            is_correct = (idx == correct_idx)
            
            if is_correct:
                correct_count += 1
            
            new_ans = StudentAnswer(
                question_id=q_id,
                attempt_id=attempt.id,
                selected_choice_index=idx,
                is_correct=is_correct
            )
            answers_to_save.append(new_ans)

        # 3. Final Score Calculation
        final_score = correct_count * points_per_question
        
        # Save everything
        ExamRepository.save_answers_and_score(attempt, answers_to_save, final_score)
        
        return {
            "score": final_score,
            "total_grade": attempt.session.total_grade, # e.g., "16" (out of 20)
            "correct_answers": correct_count,
            "status": "Submitted"
        }, None
    

    @staticmethod
    def get_exam_results(professor_id, session_id):
        session = ExamRepository.get_session_by_id(session_id)
        
        if not session:
            return None, "Session not found"
            
        if session.professor_id != professor_id:
            return None, "Unauthorized: You did not create this exam."

        results = []
        for attempt in session.attempts:
            # Skip students who joined but haven't finished
            status = "Finished" if attempt.finished_at else "In Progress"
            
            # Fetch student name
            student_name = f"{attempt.user.first_name} {attempt.user.last_name}"
            
            results.append({
                "student_id": attempt.user_id,
                "student_name": student_name,
                "score": attempt.score,
                "total": session.total_grade,
                "status": status,
                "submitted_at": attempt.finished_at.isoformat() if attempt.finished_at else None
            })
            
        return results, None