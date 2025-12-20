from src.extensions import db
from .models import Branch

class BranchRepository:
    @staticmethod
    def create(branch):
        db.session.add(branch)
        db.session.commit()
        return branch

    @staticmethod
    def get_all():
        return Branch.query.all()

    @staticmethod
    def get_by_id(branch_id):
        return Branch.query.get(branch_id)

    @staticmethod
    def get_by_name(name):
        return Branch.query.filter_by(name=name).first()
    
    @staticmethod
    def delete(branch):
        db.session.delete(branch)
        db.session.commit()