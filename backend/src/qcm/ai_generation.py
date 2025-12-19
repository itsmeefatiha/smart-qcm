import os
import json
import random
import google.generativeai as genai

class AIGenerator:
    @staticmethod
    def generate(text_content, num_questions=5, level="medium"):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return None, "Google API Key is missing in .env"

        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.7,
            }
        )

        # I updated the prompt slightly to explicitly ask for randomization too
        prompt = f"""
        You are a university professor. Generate {num_questions} multiple-choice questions (QCM) based on the text below.
        Difficulty: {level}
        Language: French.

        IMPORTANT: 
        1. Randomize the position of the correct answer for each question. Do not always put it in the same spot.
        2. Ensure distractors (wrong answers) are plausible.

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

            # --- THE MAGIC FIX: Python Side Shuffling ---
            # This guarantees the correct answer is always at a random position
            # regardless of what the AI did.
            for q in questions_data:
                random.shuffle(q['choices'])
            
            return questions_data, None

        except Exception as e:
            return None, f"AI Error: {str(e)}"