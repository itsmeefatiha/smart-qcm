from datetime import datetime
from src.extensions import db
from .models import Attempt, AnswerStudent, SessionExamen
from src.IA.models import Question, Choice


def get_correct_answers(qcm_id: int) -> dict:
    """
    Récupère les bonnes réponses d'un QCM depuis la DB.
    Retour:
    {
        question_id: correct_choice_id
    }
    """
    questions = Question.query.filter_by(qcm_id=qcm_id).all()
    correct = {}
    for q in questions:
        correct_choice = Choice.query.filter_by(question_id=q.id, is_correct=True).first()
        if correct_choice:
            correct[q.id] = correct_choice.id
    return correct


def correct_exam(attempt_id: int, answers_payload: list):
    attempt = Attempt.query.get(attempt_id)
    session = SessionExamen.query.get(attempt.session_id)

    # 1️⃣ récupérer les bonnes réponses (MOCK)
    correct_answers = get_correct_answers(session.qcm_id)

    score = 0
    total = len(correct_answers)

    # 2️⃣ enregistrer les réponses
    for ans in answers_payload:
        answer = AnswerStudent(
            attempt_id=attempt.id,
            question_id=ans["question_id"],
            response_id=ans["response_id"]
        )
        db.session.add(answer)

        # 3️⃣ correction
        if correct_answers.get(ans["question_id"]) == ans["response_id"]:
            score += 1

    # 4️⃣ calcul note sur 20
    if total == 0:
        attempt.score = 0
    else:
        attempt.score = (score / total) * 20
    attempt.finished_at = datetime.utcnow()

    db.session.commit()
    return attempt.score
