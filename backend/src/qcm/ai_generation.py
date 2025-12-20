import os
import json
import random
import google.generativeai as genai

class AIGenerator:
    @staticmethod
    def generate(text_content, num_questions=5, level="medium", mode="professor"):
        """
        mode: 'professor' (Official, Hard, Analytic) vs 'student' (Practice, Varied, Basic)
        """
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return None, "Google API Key is missing in .env"

        genai.configure(api_key=api_key)
        
        # STRATEGY 1: TEMPERATURE
        # Professor = Lower (0.3) -> More deterministic, precise, formal.
        # Student = Higher (0.9) -> More random, ensures different questions every time they click generate.
        temperature = 0.3 if mode == "professor" else 0.9

        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            generation_config={
                "response_mime_type": "application/json",
                "temperature": temperature,
            }
        )

        # STRATEGY 2: PROMPT ENGINEERING (The "Anti-Overlap" Logic)
        if mode == "professor":
            role_instruction = """
            You are a strict University Examiner creating a FINAL EXAM.
            Your goal is to test DEEP UNDERSTANDING, ANALYSIS, and SYNTHESIS.
            - Avoid simple definitions.
            - Create complex scenarios or edge-case questions.
            - Make distractors (wrong answers) very tricky and plausible.
            """
        else: # Student Mode
            role_instruction = """
            You are a Tutor creating a PRACTICE DRILL for a student.
            Your goal is to test MEMORY, KEY DEFINITIONS, and BASIC CONCEPTS.
            - Focus on facts, vocabulary, and direct application.
            - Questions should help them learn, not trick them.
            - ensure questions cover different random parts of the text to avoid repetition.
            """

        prompt = f"""
        {role_instruction}
        
        Generate {num_questions} multiple-choice questions (QCM) based on the text below.
        Difficulty: {level}
        Language: French.

        IMPORTANT: 
        1. Randomize the position of the correct answer for each question.
        2. Ensure distractors are plausible.

        OUTPUT SCHEMA (JSON Array):
        [
          {{
            "text": "Question text",
            "choices": [
               {{ "text": "Option A", "is_correct": false }},
               {{ "text": "Option B", "is_correct": true }},
               {{ "text": "Option C", "is_correct": false }},
               {{ "text": "Option D", "is_correct": false }}
            ]
          }}
        ]

        SOURCE TEXT:
        {text_content[:50000]} 
        """

        try:
            response = model.generate_content(prompt)
            questions_data = json.loads(response.text)

            # Python-side shuffling (Always keep this)
            for q in questions_data:
                random.shuffle(q['choices'])
            
            return questions_data, None

        except Exception as e:
            return None, f"AI Error: {str(e)}"