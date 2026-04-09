from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from src.auth.decorators import role_required
from src.users.models import UserRole
from .service import SchoolService
from . import school_bp

@school_bp.route('/branches', methods=['GET'])
# Optional: @jwt_required() -> Uncomment if you want public access
@swag_from({
    'tags': ['School'],
    'summary': 'List available branches',
    'responses': {
        200: {'description': 'List of branches'},
    },
})
def list_branches():
    """
    Public endpoint so students can see branches during registration.
    """
    branches = SchoolService.get_all_branches()
    return jsonify([b.to_dict() for b in branches]), 200

@school_bp.route('/branches/<int:branch_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['School'],
    'summary': 'Get a branch by ID',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'path',
        'name': 'branch_id',
        'type': 'integer',
        'required': True,
    }],
    'responses': {
        200: {'description': 'Branch details'},
        404: {'description': 'Branch not found'},
    },
})
def get_branch(branch_id):
    branch, error = SchoolService.get_branch_by_id(branch_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(branch.to_dict()), 200

@school_bp.route('/branch', methods=['POST'])
@role_required([UserRole.MANAGER, UserRole.ADMIN]) 
@swag_from({
    'tags': ['School'],
    'summary': 'Create a new branch',
    'security': [{'BearerAuth': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['name'],
            'properties': {
                'name': {'type': 'string'},
                'description': {'type': 'string'},
            },
        },
    }],
    'responses': {
        201: {'description': 'Branch created successfully'},
        400: {'description': 'Validation error'},
        403: {'description': 'Unauthorized'},
    },
})
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