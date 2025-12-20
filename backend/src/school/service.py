from .repository import BranchRepository
from .models import Branch

class SchoolService:
    @staticmethod
    def create_branch(data):
        name = data.get('name')
        description = data.get('description')

        if not name:
            return None, "Branch name is required"

        # 1. Check for duplicates
        if BranchRepository.get_by_name(name):
            return None, f"Branch '{name}' already exists."

        # 2. Create Object
        new_branch = Branch(name=name, description=description)
        
        # 3. Save
        try:
            saved_branch = BranchRepository.create(new_branch)
            return saved_branch, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_all_branches():
        return BranchRepository.get_all()

    @staticmethod
    def get_branch_by_id(branch_id):
        branch = BranchRepository.get_by_id(branch_id)
        if not branch:
            return None, "Branch not found"
        return branch, None