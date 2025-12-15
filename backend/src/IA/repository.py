from src.extensions import db
from src.IA.models import QCM, Question, Choice

class IARepository:
    @staticmethod
    def add(qcm: QCM) -> QCM:
        db.session.add(qcm)
        db.session.commit()
        return qcm
