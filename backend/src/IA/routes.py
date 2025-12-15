
from fastapi import APIRouter
from ia.schemas import QCMRequest, QCMResponse
from ia.service import generate_qcm

router = APIRouter()

@router.post("/generate_qcm", response_model=QCMResponse)
def generate_qcm_endpoint(request: QCMRequest):
    questions = generate_qcm(
        text=request.text,
        role=request.role,
        difficulty=request.difficulty
    )
    # Ici on pourrait insérer en base et récupérer qcm_id
    qcm_id = 1  # placeholder
    return QCMResponse(qcm_id=qcm_id, questions=questions)
