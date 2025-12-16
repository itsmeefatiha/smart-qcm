from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random
import string

from src.extensions import db
from .models import SessionExamen, Attempt
from .service import correct_exam

exams_bp = Blueprint("exams", __name__, url_prefix="/exams")


def generate_code():
    return "EXAM-" + "".join(random.choices(string.digits, k=4))


@exams_bp.route("/sessions", methods=["POST"])
def create_session():
    data = request.json

    session = SessionExamen(
        code=generate_code(),
        qcm_id=data["qcm_id"],
        duration_minutes=data["duration"],
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=data["duration"]),
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({"code": session.code}), 201


@exams_bp.route("/join", methods=["POST"])
def join_session():
    data = request.json
    session = SessionExamen.query.filter_by(code=data["code"]).first()

    if not session or not session.is_active:
        return jsonify({"error": "Session invalide"}), 400

    attempt = Attempt(
        session_id=session.id,
        student_id=data.get("student_id", 1)  # MOCK student
    )

    db.session.add(attempt)
    db.session.commit()

    return jsonify({"attempt_id": attempt.id}), 200


@exams_bp.route("/submit", methods=["POST"])
def submit_exam():
    data = request.json
    score = correct_exam(data["attempt_id"], data["answers"])
    return jsonify({"score": score}), 200
