from sqlalchemy import func, case, desc
from src.school.models import Branch
from src.qcm.models import Question
from src.extensions import db
from src.users.models import User, UserRole
from src.exams.models import StudentAnswer, StudentAttempt, ExamSession

class StatsRepository:
    @staticmethod
    def count_users_by_role(role):
        return User.query.filter_by(role=role).count()

    @staticmethod
    def count_total_exams():
        return ExamSession.query.count()

    @staticmethod
    def count_total_attempts():
        return StudentAttempt.query.count()

    @staticmethod
    def get_global_average_score():
        # Returns a scalar value (e.g., 14.5) or None
        return db.session.query(func.avg(StudentAttempt.score)).scalar() or 0

    @staticmethod
    def get_attempts_by_branch(branch_id):
        """
        Joins StudentAttempt -> User to filter by User's branch_id
        """
        return db.session.query(StudentAttempt).join(User).filter(
            User.branch_id == branch_id
        ).all()
    
    @staticmethod
    def get_hardest_questions(limit=5):
        """
        Calculates the percentage of WRONG answers for each question.
        Returns top 'limit' questions where students struggle the most.
        """
        # Formula: (Count of Wrong Answers / Total Answers) * 100
        return db.session.query(
            Question.text,
            func.count(StudentAnswer.id).label('total'),
            func.sum(case((StudentAnswer.is_correct == False, 1), else_=0)).label('wrong')
        ).join(StudentAnswer)\
         .group_by(Question.id)\
         .having(func.count(StudentAnswer.id) > 0)\
         .order_by(desc('wrong'))\
         .limit(limit)\
         .all()

    @staticmethod
    def get_completion_stats():
        """
        Compares Total Attempts vs. Finished Attempts (Submitted).
        """
        total = db.session.query(func.count(StudentAttempt.id)).scalar()
        finished = db.session.query(func.count(StudentAttempt.id))\
                     .filter(StudentAttempt.finished_at != None).scalar()
        
        return total, finished

    @staticmethod
    def get_average_score_by_branch():
        """
        Groups all attempts by Branch and calculates the average score for each.
        Returns: [('Big Data', 14.5), ('Software Eng', 12.3), ...]
        """
        return db.session.query(
            Branch.name,
            func.avg(StudentAttempt.score)
        ).join(User, User.branch_id == Branch.id)\
         .join(StudentAttempt, StudentAttempt.user_id == User.id)\
         .group_by(Branch.name)\
         .all()