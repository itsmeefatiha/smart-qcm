# test/tst3_gemini.py

import os
import sys
import json
# Importe 'load_dotenv' pour lire le fichier .env
from dotenv import load_dotenv 

# --- GESTION DU CHEMIN (CORRECTE pour votre architecture) ---
# Ajoute le répertoire PARENT (backend) au chemin de recherche
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..')) 
if project_root not in sys.path:
    sys.path.append(project_root)
# ------------------------------------------------------------

# Charge les variables d'environnement (y compris GEMINI_API_KEY)
load_dotenv() 

try:
    # Importation isolée et directe du fichier du modèle Gemini
    # Ceci est le chemin correct : dossier_racine/src/dossier_module/fichier
    from src.ia.gemini_model import GeminiQCMGenerator
    
except ImportError as e:
    print("-" * 50)
    print(f"❌ ÉCHEC DE L'IMPORTATION. Erreur: {e}")
    print("Vérifications à effectuer:")
    print("1. Le dossier 'ia' est-il en minuscules et contient-il un __init__.py ?")
    print("2. Tous les dossiers parents (src) contiennent-ils un __init__.py ?")
    print("3. Si l'erreur est 'No module named src', modifiez les imports internes dans vos modules (par ex. ia/models.py) de 'from src.extensions' à 'from extensions'.")
    sys.exit(1)


def run_gemini_test():
    """
    Teste la connexion à Gemini et la génération d'un QCM structuré.
    """
    print("🚀 Démarrage du test d'intégration Gemini...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ÉCHEC: La variable d'environnement GEMINI_API_KEY n'est pas définie.")
        return

    TEXTE_SOURCE = """
    Le protocole HTTP (Hypertext Transfer Protocol) est la base du World Wide Web. 
    Il fonctionne sur un modèle client-serveur. Le client (généralement un navigateur) 
    envoie une requête HTTP au serveur. Le serveur traite la requête et renvoie une 
    réponse. La requête contient une méthode (GET, POST, etc.) et une URL. 
    La réponse contient un code de statut (200 OK, 404 Not Found, etc.) et les données demandées.
    """
    
    TITRE_QCM = "Introduction au Protocole HTTP"
    NB_QUESTIONS = 2
    
    try:
        # Initialisation du générateur
        generator = GeminiQCMGenerator(api_key=api_key)
        
        print(f"   -> Appel de Gemini pour générer {NB_QUESTIONS} questions...")
        
        qcm_json = generator.generate_qcm_json(
            document_text=TEXTE_SOURCE, 
            title=TITRE_QCM, 
            num_questions=NB_QUESTIONS
        )

        if qcm_json:
            print("✅ SUCCÈS: Réponse JSON de Gemini reçue.")
            
            print("\n--- Aperçu du QCM Généré (Format JSON) ---")
            print(json.dumps(qcm_json, indent=2))
            print("-" * 50)
                
            print("\nTest terminé avec succès. L'intégration de l'IA est fonctionnelle.")
            
        else:
            print("❌ ÉCHEC: Le modèle Gemini n'a pas pu générer de réponse JSON valide.")

    except Exception as e:
        print(f"❌ ÉCHEC FATAL: Une erreur inattendue s'est produite: {e}")


if __name__ == "__main__":
    run_gemini_test()