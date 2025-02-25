import asyncio
import os
from dotenv import load_dotenv
from llm_utils import GeminiHandler

async def main():
    # Initialize the Gemini handler
    gemini = GeminiHandler()
    
    print("Testing Gemini API connection...")
    
    # Test basic connection
    if gemini.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        return
    
    # Test insurance recommendation
    print("\nTesting insurance recommendation generation...")
    test_user = {
        'age': 35,
        'budget': 2000,
        'family_size': 3,
        'medical_history': 'No major health issues'
    }
    
    try:
        recommendation = await gemini.generate_insurance_recommendation(test_user)
        print("\nGenerated Recommendation:")
        print("-" * 50)
        print(recommendation)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Error generating recommendation: {str(e)}")
    
    # Test feedback analysis
    print("\nTesting feedback analysis...")
    test_feedback = "I'm very satisfied with the insurance plan. The coverage is excellent and the price is reasonable."
    
    try:
        analysis = await gemini.analyze_feedback(test_feedback)
        print("\nFeedback Analysis:")
        print("-" * 50)
        print(analysis['analysis'])
        print("-" * 50)
    except Exception as e:
        print(f"❌ Error analyzing feedback: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
