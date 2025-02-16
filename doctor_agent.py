# doctor_agent.py

import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()  # Load API keys from .env

class DoctorAgent:
    def __init__(self):
        self.ai_ml_api_key = os.getenv("AI_ML_API_KEY")
        self.endpoint = os.getenv("AI_ML_API_ENDPOINT")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

    def diagnose_plant(self, plant_image, context_data):
        """
        Sends the plant image to the AI/ML API for real-time diagnosis.
        """
        if not plant_image:
            return "No image provided. Unable to diagnose."
        try:
            files = {"image": plant_image.getvalue()}
            params = {"apikey": self.ai_ml_api_key}
            response = requests.post(self.endpoint, files=files, params=params)
            if response.status_code == 200:
                result = response.json()
                disease = result.get("disease", "No disease detected")
                confidence = result.get("confidence", 0)
                recommendations = result.get("recommendations", "No recommendations provided")
                return f"Disease: {disease}\nConfidence: {confidence}%\nRecommendations: {recommendations}"
            else:
                return f"Error: API responded with status code {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

    def chat_assistant(self, plant_image, query, context_data):
        """
        Uses the plant image to obtain a diagnosis and then leverages OpenAI's Chat API
        to provide additional insights based on the user's follow-up query.
        """
        diagnosis = self.diagnose_plant(plant_image, context_data)
        prompt = (
            f"Plant Diagnosis:\n{diagnosis}\n\n"
            f"User Query: {query}\n"
            "Provide detailed advice regarding the plant's condition and next steps."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a plant health expert and agricultural advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            return answer
        except Exception as e:
            return f"Error in chat assistant: {str(e)}"
