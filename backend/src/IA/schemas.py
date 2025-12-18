
from pydantic import BaseModel
from typing import List

class QCMRequest(BaseModel):
    user_id: int
    document_id: int
    role: str            # "Prof" ou "Etudiant"
    difficulty: str      # "easy", "medium", "hard"
    # text removed, fetched from document

class Choice(BaseModel):
    text: str
    is_correct: bool

class Question(BaseModel):
    text: str
    choices: List[Choice]

class QCMResponse(BaseModel):
    qcm_id: int
    questions: List[Question]
