from src.extensions import db
from .models import QCM, Question, Choix

class QCMRepository:
    @staticmethod
    def create_qcm(title, document_id, user_id, questions_data):
        # Création de l'entité QCM
        new_qcm = QCM(
            title=title, 
            document_id=document_id, 
            user_id=user_id
        )
        db.session.add(new_qcm)
        db.session.flush() # Assurer que l'ID du QCM est généré

        # Création des Questions et des Choix
        for q_data in questions_data:
            new_question = Question(
                text=q_data['question_text'],
                qcm_id=new_qcm.id
            )
            db.session.add(new_question)
            db.session.flush() # Assurer que l'ID de la Question est généré

            for c_data in q_data['choices']:
                new_choix = Choix(
                    text=c_data['choice_text'],
                    is_correct=c_data['is_correct'],
                    question_id=new_question.id
                )
                db.session.add(new_choix)

        db.session.commit()
        return new_qcm

    @staticmethod
    def get_qcm_by_id(qcm_id):
        return QCM.query.get(qcm_id)

    @staticmethod
    def get_all_by_user(user_id):
        return QCM.query.filter_by(user_id=user_id).order_by(QCM.generation_date.desc()).all()