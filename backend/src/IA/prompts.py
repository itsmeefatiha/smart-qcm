

def get_prompt(role: str, difficulty: str, text: str, num_questions: int = 5) -> str:
    return f"""
Rôle: {role}
Niveau de difficulté: {difficulty}

Texte du document :
{text}

Tâche: Génère {num_questions} questions QCM avec 4 options chacune et indique la bonne réponse.
"""
