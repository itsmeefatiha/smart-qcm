import os
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError

class GeminiQCMGenerator:
    def __init__(self, api_key=None):
        # Utiliser la clé de l'environnement ou celle passée
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY n'est pas définie. Veuillez configurer votre clé API.")
        
        self.client = genai.Client(api_key=key)
        self.model = 'gemini-2.5-flash' # Modèle rapide et efficace

    def generate_qcm_json(self, document_text: str, title: str, num_questions: int = 5):
        """
        Appelle l'API Gemini pour générer un QCM à partir d'un texte.
        """
        # Définition du schéma de sortie pour garantir la structure JSON
        qcm_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "qcm_title": types.Schema(type=types.Type.STRING, description=f"Titre du QCM basé sur le titre: '{title}'"),
                "questions": types.Schema(
                    type=types.Type.ARRAY,
                    description=f"Liste de {num_questions} questions à choix multiples générées à partir du texte.",
                    items=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "question_text": types.Schema(type=types.Type.STRING, description="Le libellé de la question."),
                            "choices": types.Schema(
                                type=types.Type.ARRAY,
                                description="Liste de 4 choix de réponse pour la question. Une seule doit être 'is_correct' = true.",
                                items=types.Schema(
                                    type=types.Type.OBJECT,
                                    properties={
                                        "choice_text": types.Schema(type=types.Type.STRING, description="Le libellé du choix de réponse."),
                                        "is_correct": types.Schema(type=types.Type.BOOLEAN, description="Vrai si ce choix est la bonne réponse, Faux sinon.")
                                    },
                                    required=["choice_text", "is_correct"]
                                )
                            )
                        },
                        required=["question_text", "choices"]
                    )
                )
            },
            required=["qcm_title", "questions"]
        )

        # Instructions du système pour guider le modèle
        system_instruction = (
            "Vous êtes un expert en création de QCM pédagogiques. "
            "Générez un QCM à choix multiples (MCQ) de haute qualité basé UNIQUEMENT sur le document fourni. "
            f"Le QCM doit contenir exactement {num_questions} questions. Chaque question doit avoir 4 choix. "
            "Assurez-vous qu'un et un seul choix est marqué comme 'is_correct': true. "
            "Le format de sortie doit être un objet JSON valide qui respecte le schéma strict donné."
        )

        prompt = (
            f"Veuillez générer un QCM. Titre suggéré: '{title}'. Nombre de questions: {num_questions}. "
            f"Voici le texte source du cours: \n\n---\n\n{document_text}"
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json", # Demande de réponse JSON
            response_schema=qcm_schema
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            
            # Le contenu est une chaîne JSON
            return json.loads(response.text)

        except APIError as e:
            print(f"Erreur API Gemini: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON de la réponse Gemini: {e}")
            print(f"Réponse brute: {response.text}")
            return None
        except Exception as e:
            print(f"Erreur inattendue lors de l'appel à Gemini: {e}")
            return None