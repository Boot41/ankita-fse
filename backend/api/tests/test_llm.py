import os
import unittest
from django.test import TestCase
from api.llm_utils import GeminiHandler

class TestGeminiIntegration(TestCase):
    def setUp(self):
        """Set up test environment."""
        self.gemini = GeminiHandler()
        self.test_user_data = {
            'age': 35,
            'budget': 2000,
            'family_size': 3,
            'medical_history': 'No major health issues'
        }

    def test_connection(self):
        """Test if Gemini API connection is working."""
        self.assertTrue(self.gemini.test_connection())

    async def test_insurance_recommendation(self):
        """Test insurance recommendation generation."""
        recommendation = await self.gemini.generate_insurance_recommendation(self.test_user_data)
        self.assertIsNotNone(recommendation)
        self.assertIsInstance(recommendation, str)
        self.assertGreater(len(recommendation), 0)

    async def test_feedback_analysis(self):
        """Test feedback analysis."""
        test_feedback = "I'm very satisfied with the insurance plan. The coverage is excellent and the price is reasonable."
        analysis = await self.gemini.analyze_feedback(test_feedback)
        self.assertIsNotNone(analysis)
        self.assertIsInstance(analysis, dict)
        self.assertIn('analysis', analysis)
        self.assertIn('original_feedback', analysis)

if __name__ == '__main__':
    unittest.main()
