from datetime import datetime
from .repository import ExamRepository
from .models import ExamSession, StudentAnswer
from src.qcm.repository import QCMRepository 
from src.qcm.models import Question # Needed to check correct answers

class ExamService:
    @staticmethod
    def create_exam_session(professor_id, data):
        # 1. Validation: Ensure QCM exists
        qcm_id = data.get('qcm_id')
        qcm = QCMRepository.get_by_id(qcm_id)
        if not qcm:
            return None, "QCM not found"
            
        # 2. Validation: Ensure Duration is possible
        question_count = len(qcm.questions)
        if question_count == 0:
            return None, "Cannot create an exam for a QCM with 0 questions."
            
        duration_minutes = data.get('duration_minutes', 60)
        
        # Calculate strict minimum (e.g., 10 seconds per question)
        min_minutes = (question_count * 10) / 60 
        if duration_minutes < min_minutes:
            return None, f"Duration is too short! Need at least {int(min_minutes)+1} minutes for {question_count} questions."
        # 1. Capture the Total Grade (default to 20 if not sent)
        data['total_grade'] = data.get('total_grade', 20)     
        data['professor_id'] = professor_id
        return ExamRepository.create_session(data), None

    @staticmethod
    def join_exam(student_id, code):
        session = ExamRepository.get_session_by_code(code)
        if not session:
            return None, "Invalid or inactive session code."

        now = datetime.utcnow()
        if now < session.start_time or now > session.end_time:
            return None, "Exam is not currently open."

        # --- ONE ATTEMPT RULE ---
        existing_attempt = ExamRepository.get_student_attempt(student_id, session.id)
        
        attempt = None
        if existing_attempt:
            if existing_attempt.finished_at is not None:
                return None, "You have already submitted this exam."
            attempt = existing_attempt # Resume
        else:
            attempt = ExamRepository.create_attempt(student_id, session.id)

        # --- DYNAMIC TIME CALCULATION ---
        # We calculate this NOW and send it to the frontend
        total_seconds = session.duration_minutes * 60
        question_count = len(session.qcm.questions)
        
        # Avoid division by zero
        seconds_per_question = int(total_seconds / question_count) if question_count > 0 else 0

        # We return the attempt + the calculated timing for the UI
        return {
            "attempt": attempt,
            "qcm": session.qcm.to_dict(),
            "config": {
                "total_duration": session.duration_minutes,
                "seconds_per_question": seconds_per_question
            }
        }, None
    
    @staticmethod
    def get_active_sessions_for_student(user_branch=None):
        # Optional: You could filter by the student's branch if you wanted
        now = datetime.utcnow()
        
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