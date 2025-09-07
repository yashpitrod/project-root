import json
import pandas as pd
import numpy as np
from datetime import datetime
from config import Config

# Import ML components
try:
    from ml_models.predictor import MLInvestmentPredictor
    ML_AVAILABLE = True
    print("✅ ML models available")
except ImportError as e:
    print(f"⚠️ ML models not available: {e}")
    ML_AVAILABLE = False

class SimpleInvestmentAdvisor:
    def __init__(self):
        self.config = Config()
        
        # Initialize ML predictor if available
        if ML_AVAILABLE:
            try:
                self.ml_predictor = MLInvestmentPredictor()
                self.use_ml = True
                print("🤖 ML-powered advisor initialized")
            except Exception as e:
                print(f"⚠️ ML initialization failed: {e}")
                self.ml_predictor = None
                self.use_ml = False
        else:
            self.ml_predictor = None
            self.use_ml = False
    
    def generate_simple_recommendation(self, user_profile):
        """Generate investment recommendations (ML-powered or rule-based)"""
        income = user_profile['avg_monthly_income']
        expenses = user_profile['monthly_expenses']
        surplus = income - expenses
        
        # Check if surplus exists
        if surplus <= 0:
            return {
                'status': 'insufficient_surplus',
                'message': 'First reduce your expenses or increase your income. You need surplus money to invest.',
                'suggestions': [
                    'Track your monthly expenses carefully',
                    'Cut down on unnecessary expenses',
                    'Look for additional income sources',
                    'Develop skills to get a better paying job'
                ]
            }
        
        # Try ML prediction first
        if self.use_ml and self.ml_predictor:
            try:
                print("🤖 Using ML-powered recommendation engine...")
                ml_result = self.ml_predictor.generate_ml_recommendations(user_profile)
                
                # Add ML indicator to response
                ml_result['recommendation_type'] = 'ML-Powered'
                ml_result['user_profile'] = user_profile
                
                return ml_result
                
            except Exception as e:
                print(f"🔄 ML prediction failed, falling back to rule-based: {e}")
                # Fall back to rule-based approach
        
        # Rule-based recommendation (fallback)
        print("📊 Using rule-based recommendation engine...")
        return self.generate_rule_based_recommendation(user_profile)
    
    def generate_rule_based_recommendation(self, user_profile):
        """Original rule-based recommendation system"""
        # ... (keep your existing rule-based logic here)
        # This is the same logic you had before
        
        income = user_profile['avg_monthly_income']
        expenses = user_profile['monthly_expenses']
        surplus = income - expenses
        age = user_profile['age']
        dependents = user_profile['dependents']
        stability = user_profile['income_stability']
        
        recommendations = []
        
        # Emergency Fund (Priority 1)
        emergency_needed = min(expenses * 3, surplus * 0.4)
        if emergency_needed >= 500:
            recommendations.append({
                'priority': 1,
                'investment_type': 'emergency_fund',
                'amount': emergency_needed,
                'percentage': (emergency_needed / surplus) * 100,
                'reason': 'Keep money for emergencies like job loss or medical emergencies',
                'how_to_start': 'Keep in savings account or liquid mutual fund for immediate access',
                'expected_return': 4.0
            })
        
        remaining_surplus = surplus - emergency_needed
        
        if remaining_surplus <= 0:
            return {
                'status': 'success',
                'total_surplus': surplus,
                'recommendations': recommendations,
                'summary': self.generate_summary(recommendations, surplus),
                'recommendation_type': 'Rule-based',
                'user_profile': user_profile
            }
        
        # Rest of rule-based logic...
        # (Include your existing logic here)
        
        return {
            'status': 'success',
            'total_surplus': surplus,
            'recommendations': recommendations,
            'summary': self.generate_summary(recommendations, surplus),
            'recommendation_type': 'Rule-based'
        }
    
    # ... (keep all your existing methods like generate_summary, get_detailed_explanation, etc.)