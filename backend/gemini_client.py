import os
import google.generativeai as genai
from typing import Optional, Dict, Any
from django.conf import settings

# Configure Gemini API
def configure_gemini():
    """Configure Gemini API with the API key from Django settings."""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError('GEMINI_API_KEY not set in Django settings')
    genai.configure(api_key=api_key)

def get_insurance_recommendation(user_data: Dict[str, Any]) -> str:
    """Get insurance plan recommendations using Gemini.
    
    Args:
        user_data: Dictionary containing user information like age, budget, etc.
        
    Returns:
        str: AI-generated insurance recommendation
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct the prompt
        prompt = f"""Based on the following user information, provide personalized health insurance recommendations:
        - Age: {user_data.get('age', 'Not specified')}
        - Budget: ${user_data.get('budget', 'Not specified')}
        - Family Size: {user_data.get('family_size', 'Not specified')}
        - Medical History: {user_data.get('medical_history', 'Not specified')}
        
        Please provide a detailed recommendation including:
        1. Type of plan that would be most suitable
        2. Coverage recommendations
        3. Cost considerations
        4. Important factors to consider
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error generating recommendation: {str(e)}"

def analyze_insurance_plan(plan_data: Dict[str, Any]) -> str:
    """Analyze an insurance plan using Gemini.
    
    Args:
        plan_data: Dictionary containing plan details
        
    Returns:
        str: AI-generated analysis of the insurance plan
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Analyze the following health insurance plan and provide insights:
        - Plan Name: {plan_data.get('name')}
        - Coverage: {plan_data.get('coverage')}
        - Price: ${plan_data.get('price')}
        - Conditions: {plan_data.get('conditions')}
        
        Please provide:
        1. Key benefits of this plan
        2. Potential limitations or drawbacks
        3. Who this plan would be most suitable for
        4. Cost-benefit analysis
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error analyzing plan: {str(e)}"