import os
import json
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

        prompt = f"""
        You are a university professor. Generate {num_questions} multiple-choice questions (QCM) based on the text below.
        Difficulty: {level}
        Language: French.

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
        # Note: We limit text to 50k chars to stay safe, though Gemini can handle more.

        try:
            response = model.generate_content(prompt)
            # Gemini returns a string, we parse it into a real Python list
            return json.loads(response.text), None
        except Exception as e:
            return None, f"AI Error: {str(e)}"