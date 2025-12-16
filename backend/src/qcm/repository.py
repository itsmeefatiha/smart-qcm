from src.extensions import db
from .models import QCM, Question

class QCMRepository:
    @staticmethod
    def create_qcm_with_questions(qcm_data, questions_list):
        try:
            # 1. Create the Exam header
            new_qcm = QCM(
                title=qcm_data['title'],
                level=qcm_data['level'],
                user_id=qcm_data['user_id'],
                document_id=qcm_data['document_id']
            )
            db.session.add(new_qcm)
            db.session.flush() # Flush to get the new_qcm.id before commit

            # 2. Create each Question
            for q_data in questions_list:
                new_question = Question(
                    text=q_data['text'],
                    choices=q_data['choices'], # Saved as JSON automatically
                    qcm_id=new_qcm.id
                )
                db.session.add(new_question)

            db.session.commit()
            return new_qcm
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(qcm_id):
        return QCM.query.get(qcm_id)

    @staticmethod
    def get_by_user(user_id):
        return QCM.query.filter_by(user_id=user_id).order_by(QCM.created_at.desc()).all()