# ia/service.py
from ia import prompts, model
from ia.schemas import Question, Choice
import re

def clean_text(text: str) -> str:
    return text.replace("\n", " ").strip()

def parse_qcm_output(output_text: str):
    """
    Parse simple pour transformer la sortie du modèle en questions + choix
    Ici on suppose que le modèle renvoie des QCM sous format :
    Q1: Question ?
    a) Option1
    b) Option2
    c) Option3
    d) Option4 (Correct)
    """
    questions = []
    blocks = re.split(r'Q\d+:', output_text)[1:]  # ignore tout avant Q1
    for block in blocks:
        lines = block.strip().split('\n')
        q_text = lines[0].strip()
        choices = []
        for line in lines[1:]:
            line = line.strip()
            is_correct = "(Correct)" in line
            choice_text = line.replace("(Correct)", "").strip()
            choices.append(Choice(text=choice_text, is_correct=is_correct))
        questions.append(Question(text=q_text, choices=choices))
    return questions

def generate_qcm(text: str, role: str, difficulty: str, num_questions: int = 5):
    text = clean_text(text)
    prompt = prompts.get_prompt(role, difficulty, text, num_questions)
    output_text = model.generate_text(prompt)
    questions = parse_qcm_output(output_text)
    return questions
