from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import ExamService
from . import exams_bp

@exams_bp.route('/create', methods=['POST'])
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Updated to handle the (session, error) tuple return style
    session, error = ExamService.create_exam_session(user_id, data)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({
        "message": "Session created",
        "code": session.code,
        "session_id": session.id
    }), 201

@exams_bp.route('/join', methods=['POST'])
@jwt_required()
def join_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # The service now returns a result dict containing config info
    result, error = ExamService.join_exam(user_id, data.get('code'))
    
    if error:
        return jsonify({"error": error}), 400
        
    # Result contains: { "attempt": ..., "qcm": ..., "config": ... }
    return jsonify({
        "message": "Exam started",
        "attempt_id": result['attempt'].id,
        "qcm": result['qcm'], 
        "exam_config": result['config']  # <--- Frontend uses this for the Timer!
    }), 200

@exams_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    """Student submits answers"""
    # Expects: { "attempt_id": 5, "answers": [{...}] }
    data = request.get_json()
    
    result, error = ExamService.submit_exam(data.get('attempt_id'), data.get('answers'))
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify(result), 200

@exams_bp.route('/active', methods=['GET'])
@jwt_required()
def list_active_exams():
    """
    Student sees a list of all currently running exams.
    """
    # In a real app, you might get the student's branch from their profile
    # user = UserService.get_by_id(get_jwt_identity())
    
    sessions = ExamService.get_active_sessions_for_student()
    
    output = []
    for s in sessions:
        output.append({
            "session_id": s.id,
            "module_name": s.qcm.document.module, # Accessing the module name via relationships
            "title": s.qcm.title,
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat(),
            "duration": s.duration_minutes,
            "professor_name": f"{s.professor.first_name} {s.professor.last_name}"
        })
        
    return jsonify(output), 200