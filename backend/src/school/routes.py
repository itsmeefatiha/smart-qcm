from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.auth.decorators import role_required
from src.users.models import UserRole
from .service import SchoolService
from . import school_bp

@school_bp.route('/branches', methods=['GET'])
# Optional: @jwt_required() -> Uncomment if you want public access
def list_branches():
    """
    Public endpoint so students can see branches during registration.
    """
    branches = SchoolService.get_all_branches()
    return jsonify([b.to_dict() for b in branches]), 200

@school_bp.route('/branches/<int:branch_id>', methods=['GET'])
@jwt_required()
def get_branch(branch_id):
    branch, error = SchoolService.get_branch_by_id(branch_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(branch.to_dict()), 200

@school_bp.route('/branch', methods=['POST'])
@role_required([UserRole.MANAGER, UserRole.ADMIN]) 
def create_branch():
    """
    Only Managers or Admins can create new branches.
    Payload: { "name": "Big Data", "description": "..." }
    """
    data = request.get_json()
    branch, error = SchoolService.create_branch(data)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify(branch.to_dict()), 201