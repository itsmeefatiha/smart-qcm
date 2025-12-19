from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import ExamService
from . import exams_bp

# 1. CREATE EXAM (Simplified: No end_time needed)
@exams_bp.route('/create', methods=['POST'])
@jwt_required()
def create_session():
    """
    Payload: {
        "qcm_id": 1,
        "description": "Final Exam for Java",
        "start_time": "2025-12-20T09:00",  <-- Local time string
        "duration_minutes": 120,
        "total_grade": 40
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    session, error = ExamService.create_exam_session(user_id, data)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "message": "Session created successfully",
        "code": session.code,
        "session_id": session.id,
        "end_time": session.end_time.isoformat() # Returns calculated end time
    }), 201

# 2. DELETE EXAM
@exams_bp.route('/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()
    
    message, error = ExamService.delete_exam_session(user_id, session_id)
    
    if error:
        return jsonify({"error": error}), 403 # Forbidden
        
    return jsonify({"message": message}), 200

# 3. PROFESSOR DASHBOARD (List all exams, even finished ones)
@exams_bp.route('/professor/list', methods=['GET'])
@jwt_required()
def list_professor_exams():
    user_id = get_jwt_identity()
    
    sessions = ExamService.get_professor_exams(user_id)
    
    output = []
    for s in sessions:
        # Check if exam is finished
        now = datetime.now()
        status = "Active"
        if s.end_time < now:
            status = "Finished"
        elif s.start_time > now:
            status = "Scheduled"

        output.append({
            "id": s.id,
            "code": s.code,
            "title": s.qcm.title,
            "description": s.description,
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat(),
            "status": status,
            "student_count": len(s.attempts) # Helpful stat
        })
        
    return jsonify(output), 200

# ... (Keep /join, /submit, /active, /results routes unchanged) ...
@exams_bp.route('/join', methods=['POST'])
@jwt_required()
def join_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    result, error = ExamService.join_exam(user_id, data.get('code'))
    if error: return jsonify({"error": error}), 400
    return jsonify({
        "message": "Exam started",
        "attempt_id": result['attempt_id'],
        "qcm": result['qcm'], 
        "exam_config": result['exam_config']
    }), 200

@exams_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    data = request.get_json()
    result, error = ExamService.submit_exam(data.get('attempt_id'), data.get('answers'))
    if error: return jsonify({"error": error}), 400
    return jsonify(result), 200

@exams_bp.route('/active', methods=['GET'])
@jwt_required()
def list_active_exams():
    sessions = ExamService.get_active_sessions_for_student()
    output = []
    for s in sessions:
        output.append({
            "session_id": s.id,
            "module_name": s.qcm.document.module,
            "title": s.qcm.title,
            "start_time": s.start_time.isoformat() + 'Z', 
            "end_time": s.end_time.isoformat() + 'Z',
            "duration": s.duration_minutes,
            "professor_name": f"{s.professor.first_name} {s.professor.last_name}"
        })
    return jsonify(output), 200

@exams_bp.route('/<int:session_id>/results', methods=['GET'])
@jwt_required()
def view_results(session_id):
    professor_id = get_jwt_identity()
    results, error = ExamService.get_exam_results(professor_id, session_id)
    if error: return jsonify({"error": error}), 403
    return jsonify(results), 200