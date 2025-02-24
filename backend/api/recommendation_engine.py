from typing import Dict, List, Any
from .models import InsurancePlan

def calculate_plan_score(plan: InsurancePlan, user_data: Dict[str, Any]) -> float:
    """
    Calculate a suitability score for a plan based on user data.
    
    Args:
        plan: The insurance plan to evaluate
        user_data: Dictionary containing user information
        
    Returns:
        float: Suitability score between 0 and 1
    """
    score = 1.0
    
    # Budget compatibility (0.4 weight)
    if user_data.get('budget'):
        budget = float(user_data['budget'])
        if plan.price > budget:
            score *= 0.6  # Reduce score if over budget
        else:
            budget_ratio = float(plan.price) / budget
            score *= 0.6 + (0.4 * (1 - budget_ratio))  # Higher score for lower price

    # Family size consideration (0.3 weight)
    if user_data.get('family_size'):
        family_size = int(user_data['family_size'])
        if family_size > 1 and 'family' in plan.coverage.lower():
            score *= 1.3
        elif family_size == 1 and 'individual' in plan.coverage.lower():
            score *= 1.3
    
    # Age consideration (0.3 weight)
    if user_data.get('age'):
        age = int(user_data['age'])
        if age > 60 and 'senior' in plan.coverage.lower():
            score *= 1.3
        elif 18 <= age <= 60 and 'adult' in plan.coverage.lower():
            score *= 1.3
    
    return min(1.0, score)  # Cap score at 1.0

def get_recommendations(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get personalized insurance plan recommendations based on user data.
    
    Args:
        user_data: Dictionary containing user information including:
                  - budget (Decimal)
                  - age (int)
                  - family_size (int)
                  - medical_history (str)
    
    Returns:
        List[Dict]: List of recommended plans with suitability scores
    """
    plans = InsurancePlan.objects.all()
    recommendations = []
    
    for plan in plans:
        score = calculate_plan_score(plan, user_data)
        recommendation = {
            'id': plan.id,
            'name': plan.name,
            'coverage': plan.coverage,
            'price': float(plan.price),
            'price_per_month': plan.price_per_month,
            'conditions': plan.conditions,
            'suitability_score': round(score, 2)
        }
        recommendations.append(recommendation)
    
    # Sort by suitability score in descending order
    recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
    
    return recommendations[:5]  # Return top 5 recommendations
