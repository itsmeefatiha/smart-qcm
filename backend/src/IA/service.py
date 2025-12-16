from src.documents.service import DocumentService # Import du service existant
from .gemini_model import GeminiQCMGenerator
from .repository import QCMRepository
from src.extensions import db # Pour les transactions en cas de besoin

class QCMService:
    @staticmethod
    def generate_and_save_qcm(document_id: int, user_id: int, num_questions: int = 5):
        # 1. Récupérer le Document et le texte
        document = DocumentService.get_document_by_id(document_id)
        if not document:
            return None, "Document introuvable."
        
        extracted_text = document.extracted_text
        if not extracted_text:
            return None, "Texte du document vide. Veuillez le ré-extraire."
        
        # 2. Appeler le modèle Gemini pour la génération
        try:
            generator = GeminiQCMGenerator()
            # Utilise le nom de fichier comme titre par défaut
            qcm_data = generator.generate_qcm_json(
                document_text=extracted_text, 
                title=f"QCM {document.module} - {document.filename}",
                num_questions=num_questions
            )
        except ValueError as e:
            return None, str(e) # Erreur de clé API
            
        if not qcm_data:
            return None, "La génération du QCM par l'IA a échoué. Veuillez réessayer."
            
        # 3. Formater les données pour le repository
        questions_to_save = []
        for q in qcm_data.get('questions', []):
            question_data = {
                'question_text': q['question_text'],
                'choices': []
            }
            for c in q['choices']:
                question_data['choices'].append({
                    'choice_text': c['choice_text'],
                    'is_correct': c['is_correct']
                })
            questions_to_save.append(question_data)
            
        qcm_title = qcm_data.get('qcm_title', f"QCM de {document.filename}")
            
        # 4. Sauvegarder dans la base de données
        try:
            new_qcm = QCMRepository.create_qcm(
                title=qcm_title,
                document_id=document_id,
                user_id=user_id,
                questions_data=questions_to_save
            )
            return new_qcm, None
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur de sauvegarde en base de données: {str(e)}"

    @staticmethod
    def get_qcm(qcm_id):
        return QCMRepository.get_qcm_by_id(qcm_id)

    @staticmethod
    def get_user_qcms(user_id):
        return QCMRepository.get_all_by_user(user_id)