import os
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class GeminiHandler:
    def __init__(self):
        """Initialize the Gemini model."""
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini model: {str(e)}")

    async def generate_insurance_recommendation(self, user_data: Dict[str, Any]) -> str:
        """
        Generate insurance recommendations based on user data.
        
        Args:
            user_data: Dictionary containing user information like age, budget, family_size, etc.
            
        Returns:
            str: Generated recommendation
        """
        try:
            prompt = f"""
            As an insurance expert, provide a detailed recommendation for a person with the following profile:
            - Age: {user_data.get('age', 'N/A')}
            - Budget: ${user_data.get('budget', 'N/A')}
            - Family Size: {user_data.get('family_size', 'N/A')}
            - Medical History: {user_data.get('medical_history', 'N/A')}

            Please provide specific insurance recommendations considering their profile.
            Include coverage suggestions and budget considerations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate recommendation: {str(e)}")

    async def analyze_feedback(self, feedback_text: str) -> Dict[str, Any]:
        """
        Analyze user feedback using Gemini.
        
        Args:
            feedback_text: The feedback text to analyze
            
        Returns:
            Dict containing sentiment and key points
        """
        try:
            prompt = f"""
            Analyze the following insurance feedback and provide:
            1. Overall sentiment (positive/negative/neutral)
            2. Key points mentioned
            3. Any specific concerns or praise

            Feedback: {feedback_text}
            """
            
            response = self.model.generate_content(prompt)
            return {
                'analysis': response.text,
                'original_feedback': feedback_text
            }
        except Exception as e:
            raise Exception(f"Failed to analyze feedback: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test if the Gemini connection is working.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            response = self.model.generate_content("Test connection to Gemini API")
            return True if response.text else False
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
