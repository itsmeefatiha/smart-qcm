from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.auth.decorators import role_required
from src.users.models import User, UserRole
from .service import StatsService
from . import stats_bp

def ensure_manager(user_id):
    user = User.query.get(user_id)
    return user.role == UserRole.MANAGER

@stats_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard_stats():
    user_id = get_jwt_identity()
    if not ensure_manager(user_id): return jsonify({"error": "Unauthorized"}), 403
    
    return jsonify(StatsService.get_global_stats()), 200

@stats_bp.route('/branch/<int:branch_id>', methods=['GET'])
@jwt_required()
def branch_stats(branch_id):
    user_id = get_jwt_identity()
    if not ensure_manager(user_id): return jsonify({"error": "Unauthorized"}), 403
    
    return jsonify(StatsService.get_branch_performance(branch_id)), 200

@stats_bp.route('/charts/hardest-questions', methods=['GET'])
@role_required([UserRole.MANAGER, UserRole.ADMIN])
def chart_hardest_questions():
    """
    Returns top 5 questions with highest failure rate.
    Great for identifying weak topics in the curriculum.
    """
    return jsonify(StatsService.get_hardest_questions_chart()), 200

@stats_bp.route('/charts/completion-rate', methods=['GET'])
@role_required([UserRole.MANAGER, UserRole.ADMIN])
def chart_completion_rate():
    """
    Returns Pie chart data: Submitted vs Abandoned exams.
    """
    return jsonify(StatsService.get_completion_rate_chart()), 200